"""Native account controls; browser authentication is handled by the official SDK."""
import queue
import threading
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from phone_dialogs import AppWindow, messagebox, simpledialog
import webbrowser
import chatgpt_provider as provider
import lu_provider

class AccountWindow(AppWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('AI & account'); self.geometry('740x620'); self.resizable(False,False)
        self.configure(bg='#191c2b'); self.parent=parent; self.events=queue.Queue()
        self.models=[]; self.session={}; self.working=False
        self.transient(parent); self.grab_set(); self.protocol('WM_DELETE_WINDOW',self.close)
        parent.label(self,'Choose how your story is generated',20,'#dfba78').pack(pady=(20,8))
        self.current=parent.label(self,'',11); self.current.pack()
        self.update_current()
        parent.button(self,'Use local Qwen 3.5 9B Abliterated · LU Engine',self.local).pack(pady=12)
        parent.button(self,'Set LU API token',self.set_lu_token).pack(pady=2)
        parent.label(self,'ChatGPT account',16).pack(pady=(12,5))
        parent.label(self,'Online generation sends character context and conversation text to OpenAI.\nUses your eligible ChatGPT plan allowance or available credits after approval.\nYour ChatGPT password is entered only in the browser.',10,'#aaaabd').pack()
        self.info=parent.label(self,'Checking saved connection…',11,wraplength=680)
        self.info.pack(pady=12)
        row=tk.Frame(self,bg=self['bg']); row.pack()
        self.signin=parent.button(row,'Continue with ChatGPT',lambda:self.run('signin'))
        self.signin.pack(side='left',padx=5)
        self.refresh=parent.button(row,'Refresh connection',lambda:self.run('status'))
        self.refresh.pack(side='left',padx=5)
        self.signout=parent.button(row,'Disconnect',lambda:self.run('disconnect'))
        self.signout.pack(side='left',padx=5)
        self.picker=ttk.Combobox(self,state='readonly',width=62)
        self.picker.pack(pady=(18,8))
        self.use=parent.button(self,'Use selected ChatGPT model',self.use_chatgpt,True)
        self.use.pack(); self.use.config(state='disabled')
        row2=tk.Frame(self,bg=self['bg']); row2.pack(pady=12)
        parent.button(row2,'Manage ChatGPT usage',lambda:webbrowser.open('https://chatgpt.com/settings/usage')).pack(side='left',padx=5)
        parent.button(row2,'Cancel sign-in',self.cancel).pack(side='left',padx=5)
        self.after(100,self.poll); self.run('status')

    def update_current(self):
        try:
            config=provider.settings()
            self.current.config(text='Current: '+('Local Qwen 3.5 9B Abliterated' if config['provider'] in ('lu','ollama') else 'ChatGPT · '+config['model']))
        except RuntimeError as exc: self.current.config(text=str(exc))

    def run(self,method):
        if self.working: return
        self.working=True
        for b in (self.signin,self.refresh,self.signout,self.use): b.config(state='disabled')
        self.info.config(text='Complete sign-in and approve plan usage in your browser…' if method=='signin' else 'Checking connection…')
        def work():
            try:
                session=provider.bridge.call(method,timeout=620 if method=='signin' else 90)
                if method=='disconnect': provider.save_settings('lu')
                models=provider.bridge.call('models',timeout=90) if session.get('sharing') else []
                self.events.put(('ok',session,models))
            except Exception as exc: self.events.put(('error',str(exc)))
        threading.Thread(target=work,daemon=True).start()

    def poll(self):
        try:
            while True:
                event=self.events.get_nowait(); self.working=False
                for b in (self.signin,self.refresh,self.signout): b.config(state='normal')
                if event[0]=='error':
                    self.info.config(text=event[1]); self.use.config(state='disabled')
                else:
                    self.session,self.models=event[1:]
                    identity=self.session.get('identity',{})
                    label=identity.get('email') or identity.get('name') or self.session.get('profileLabel','')
                    enabled=self.session.get('sharing',False)
                    self.info.config(text=(label+' · Connected · ChatGPT plan usage enabled') if enabled else
                        ('Connected; plan usage has not been enabled.' if self.session.get('status')=='connected' else 'Not connected. Continue with ChatGPT to sign in.'))
                    self.picker['values']=[m.get('displayName',m['slug'])+' · '+m['slug'] for m in self.models]
                    if self.models:
                        selected=provider.settings().get('model','')
                        idx=next((i for i,m in enumerate(self.models) if m['slug']==selected),0)
                        self.picker.current(idx)
                    else: self.picker.set('')
                    self.use.config(state='normal' if enabled and self.models else 'disabled')
                    self.update_current()
        except queue.Empty: pass
        self.after(100,self.poll)

    def local(self):
        provider.save_settings('lu'); self.update_current()
        self.parent.model_status='Using local Qwen 3.5 9B Abliterated · LU Engine'
        self.parent.status.config(text=self.parent.model_status)

    def set_lu_token(self):
        token = simpledialog.askstring('LU Local API',
            'In Locally Uncensored: Settings > Voice & Remote > Local API.\nGenerate and copy a token, then start the API on port 8129.\nPaste the token here (stored with Windows encryption):',
            parent=self, show='*')
        if token is None:
            return
        try:
            lu_provider.save_token(token)
            self.local()
            self.info.config(text='LU token saved. Keep Locally Uncensored and its Local API running.')
        except (OSError, ValueError, RuntimeError) as exc:
            messagebox.showerror('LU Local API', str(exc), parent=self)

    def use_chatgpt(self):
        index=self.picker.current()
        if self.working or not self.session.get('sharing') or index<0: return
        provider.save_settings('chatgpt',self.models[index]['slug']); self.update_current()
        self.parent.model_status='Using ChatGPT plan · '+self.models[index]['displayName']
        self.parent.status.config(text=self.parent.model_status)
        self.info.config(text='ChatGPT selected. Close this window to continue your story.')

    def cancel(self):
        threading.Thread(target=lambda:provider.bridge.call('cancel',timeout=10),daemon=True).start()

    def close(self):
        if self.working: self.cancel()
        self.grab_release(); self.destroy()
