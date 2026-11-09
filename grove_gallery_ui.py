"""Grove profile photo grids and scrollable post details."""
import tkinter as tk
from tkinter import ttk
from functools import lru_cache
from phone_dialogs import AppWindow, find_phone
from PIL import Image, ImageTk
import grove
import grove_gallery as gallery
import phone_apps as apps
import winterfield_ui as ui


@lru_cache(maxsize=48)
def _thumbnail(path, size, modified, file_size):
    """Cache only small PIL images; never retain Tk widgets or full-size photos."""
    with Image.open(path) as source:
        source.draft('RGB', (size, size))
        image = source.convert('RGB')
        image.thumbnail((size, size), Image.Resampling.LANCZOS)
    return image


def photo_button(parent, post, size, command):
    phone = find_phone(parent)
    if phone is not None:
        size = min(size, max(120, phone.winfo_width()-90))
    try:
        path = gallery.ROOT / post['image']
        stat = path.stat()
        image = _thumbnail(str(path), size, stat.st_mtime_ns, stat.st_size)
    except (OSError, ValueError):
        return ttk.Button(parent, text='Photo unavailable · Open post', command=command)
    photo = ImageTk.PhotoImage(image, master=parent)
    button = ttk.Button(parent, image=photo, command=command)
    button.photo = photo
    return button


def like_button(parent, host, post):
    timer = None
    frame = ttk.Frame(parent)
    names_label = ttk.Label(frame, wraplength=450)
    def update():
        gallery.update_likes(host.game.state_data)
        liked = host.game.state_data['player'] in post.get('liked_by', [])
        button.configure(text=f"{'♥' if liked else '♡'} {gallery.like_count(post, host.game.state_data['player']):,} likes")
        names = [apps.handle(who, host.game.state_data) for who in post.get('liked_by', []) if who != host.game.state_data['player']]
        names_label.configure(text=('Liked by ' + ', '.join(names)) if names else '')

    def toggle():
        gallery.toggle_like(host.game.state_data, post['id'])
        host.game.persist()
        update()

    button = ttk.Button(frame, command=toggle)
    button.pack(anchor='w')
    names_label.pack(anchor='w')
    update()
    def tick():
        nonlocal timer
        update()
        timer = button.after(1000, tick)
    def cleanup(event):
        if event.widget is button and timer is not None:
            button.after_cancel(timer)
    button.bind('<Destroy>', cleanup, add='+')
    timer = button.after(1000, tick)
    return frame


def show_profile(host, who):
    window = AppWindow(host)
    window.title(f'Grove · {apps.handle(who, host.game.state_data)}')
    window.geometry('660x780')
    window.minsize(610, 500)
    heading = ttk.Frame(window, padding=16)
    heading.pack(fill='x')
    ttk.Label(heading, text=apps.handle(who, host.game.state_data), font=('Segoe UI', 19, 'bold')).pack(anchor='w')
    ttk.Label(heading, text=grove.profile(host.game.state_data, who)['bio'], wraplength=240 if window.phone else 580).pack(anchor='w', pady=6)
    posts = gallery.photos(host.game.state_data, who)
    comment_counts = {}
    for entry in apps.grove_posts(host.game.state_data):
        parent = entry.get('parent')
        comment_counts[parent] = comment_counts.get(parent, 0) + 1
    ttk.Label(heading, text=f"{grove.profile(host.game.state_data, who)['followers']:,} followers · {len(posts)} photos").pack(anchor='w')
    body = host.scroll_area(window)
    if not posts:
        ttk.Label(body, text='No photos posted yet.', padding=20).pack()
        return window
    columns = 1 if window.phone is not None else 3
    for col in range(columns):
        body.columnconfigure(col, weight=1)
    for index, post in enumerate(posts):
        card = ttk.Frame(body, padding=6)
        card.grid(row=index // columns, column=index % columns, sticky='nsew')
        photo_button(card, post, 178, lambda p=post: show_post(host, p)).pack()
        ttk.Label(card, text=gallery.timestamp(post).split(' · ')[0]).pack(anchor='w', pady=(4, 0))
        ttk.Label(card, text=f"♥ {gallery.like_count(post, host.game.state_data['player']):,} · {comment_counts.get(post['id'], 0)} comments").pack(anchor='w')
        ttk.Label(card, text=post['text'], wraplength=174).pack(anchor='w', pady=4)
    return window


def compose(host, record=None):
    """A separate composer keeps captions intact while the live feed refreshes."""
    import camera
    state = host.game.state_data
    window = AppWindow(host)
    window.title('Grove · Share a photo')
    window.geometry('560x720')
    body = host.scroll_area(window)
    content = ttk.Frame(body, padding=14)
    content.pack(fill='both', expand=True)
    if record is None:
        ttk.Label(content, text='Choose a Gallery photo', font=('Segoe UI', 16, 'bold')).pack(anchor='w')
        try:
            records = camera.photos(state)
        except (OSError, ValueError):
            records = []
        if not records:
            ttk.Label(content, text='No photos available. Take a photo in Camera first.').pack(pady=16)
            def camera_app():
                window.destroy()
                host.open_app('Camera')
            ttk.Button(content, text='Open Camera', command=camera_app).pack()
        for item in records:
            def select(item=item):
                window.destroy()
                compose(host, item)
            photo_button(content, {'image': item['path']}, 220, select).pack(pady=8)
            ttk.Button(content, text=f"{item['date']} · {item['mode']} · Choose", command=select).pack()
        return window
    photo_button(content, {'image': record['path']}, 430, lambda: None).pack(pady=8)
    ttk.Label(content, text='Caption · 1–280 characters').pack(anchor='w')
    caption = tk.Text(content, height=4, wrap='word')
    caption.pack(fill='x', pady=6)
    feedback = ttk.Label(content, wraplength=460)
    feedback.pack(fill='x')
    def publish():
        if host.game.state_data is not state:
            feedback.config(text='Your active game changed. Reopen the photo composer.')
            return
        try:
            gallery.publish(state, record['id'], caption.get('1.0', 'end-1c'))
        except (OSError, ValueError) as exc:
            feedback.config(text=str(exc))
            return
        host.game.persist()
        window.destroy()
        host.open_app('Grove')
    ttk.Button(content, text='Post photo to Grove', command=publish).pack(pady=10)
    caption.focus_set()
    return window


def show_post(host, post):
    gallery.mark_read(host.game.state_data, post['id'])
    host.game.persist()
    window = AppWindow(host)
    window.title(f"Grove post · {apps.handle(post['author'], host.game.state_data)}")
    window.geometry('650x850')
    window.minsize(570, 500)
    body = host.scroll_area(window)
    content = ttk.Frame(body, padding=14)
    content.pack(fill='x')
    ttk.Button(content, text=apps.handle(post['author'], host.game.state_data),
               command=lambda: show_profile(host, post['author'])).pack(anchor='w')
    ttk.Label(content, text=gallery.timestamp(post)).pack(anchor='w', pady=5)
    if post.get('image'):
        photo_button(content, post, 510, lambda: show_full_image(window, post)).pack(anchor='center')
    ttk.Label(content, text=post['text'], wraplength=510).pack(anchor='w', pady=10)
    like_button(content, host, post).pack(anchor='w')
    ttk.Label(content, text='Comments', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(14, 6))
    posts = apps.grove_posts(host.game.state_data)
    children = {}
    for p in posts:
        children.setdefault(p['parent'], []).append(p)
    stack = [(p, 0) for p in reversed(children.get(post['id'], []))]
    def reply(target=post):
        host.open_app('Grove')
        host.choose_reply(target)
        host.lift()
        host.grove_entry.focus_set()
        window.destroy()

    while stack:
        comment, depth = stack.pop()
        card = ttk.Frame(content, padding=6)
        card.pack(fill='x', padx=(min(depth, 4)*12, 0))
        ttk.Label(card, text=f"{apps.handle(comment['author'], host.game.state_data)} · {gallery.timestamp(comment)}",
                  wraplength=490, font=('Segoe UI', 9, 'bold')).pack(anchor='w')
        ttk.Label(card, text=comment['text'], wraplength=490-min(depth, 4)*12).pack(anchor='w', pady=3)
        ttk.Button(card, text='Reply to comment', command=lambda target=comment: reply(target)).pack(anchor='w')
        stack.extend((p, depth+1) for p in reversed(children.get(comment['id'], [])))

    ttk.Button(content, text='Write a comment in Grove', command=reply).pack(anchor='w', pady=12)
    return window


def show_notifications(host):
    window = AppWindow(host, background=ui.PANEL)
    window.title('Grove · Notifications')
    window.geometry('540x600')
    body = host.scroll_area(window)
    for notification in reversed(gallery.unread_comments(host.game.state_data)):
        card = ttk.Frame(body, padding=12)
        card.pack(fill='x')
        action = 'replied to your comment' if notification.get('kind') == 'reply' else 'commented on your post'
        ttk.Label(card, text=f"{apps.handle(notification['author'], host.game.state_data)} {action}",
                  wraplength=450).pack(anchor='w')
        ttk.Label(card, text=notification['text'], wraplength=450).pack(anchor='w', pady=6)
        def open_post(notification=notification):
            post = next((p for p in apps.grove_posts(host.game.state_data)
                         if p['id'] == notification['post_id']), None)
            if post:
                show_post(host, post)
            window.destroy()
            host.refresh_feed()
        ttk.Button(card, text='View post & comments', command=open_post).pack(anchor='w')
    return window


def show_full_image(parent, post):
    window = AppWindow(parent)
    window.title('Grove · Photo')
    size = min(window.winfo_screenheight()-150, window.winfo_screenwidth()-100, 1000)
    photo_button(window, post, size, window.destroy).pack()
    return window
