"""Dark phone job boards with private, anonymous criminal progression."""
import tkinter as tk
from tkinter import ttk
import textwrap
import job_apps as jobs
import town
import winterfield_ui as ui
import phone_theme
import organisation_logos


class JobBoard:
    def __init__(self, phone, parent, criminal=False, in_person=False, section=None, workplace_key=None):
        self.phone=phone; self.game=phone.game; self.criminal=criminal
        self.in_person=in_person; self.workplace_key=workplace_key
        self.section=section or ('Contracts' if criminal else 'Find jobs'); self.notice=''
        self.parent=parent; self.search=''; self.draw()

    def physical_action(self, fn, args):
        if self.criminal:
            import bubblegram_roles, crime_diplomacy
            return self.game.state_data['player'] in bubblegram_roles.ROLES and fn in (jobs.resolve, crime_diplomacy.settle)
        if fn == jobs.civilian.deliver and args and args[0]: return False
        return fn in (jobs.begin_shift, jobs.resolve, jobs.promote, jobs.civilian.train,
                      jobs.civilian.network, jobs.civilian.specialise, jobs.civilian.project,
                      jobs.civilian.deliver, jobs.civilian.manage)

    def open_workplace(self):
        if self.criminal:
            from bubblegram_workplace_ui import open_workplace
            open_workplace(self.game, self.section)
            return
        from jobseek_workplace_ui import open_workplace
        try: open_workplace(self.game, self.section if self.section!='Find jobs' else 'My career')
        except ValueError as exc:
            self.notice=str(exc); self.draw()

    def act(self, fn, *args):
        if not self.in_person and self.physical_action(fn,args):
            self.open_workplace(); return
        if self.game.busy: self.notice='Wait for the current conversation to finish.'
        else:
            try:
                if self.in_person and not self.criminal:
                    from jobseek_workplace_ui import require_workplace
                    require_workplace(self.game.state_data,self.workplace_key)
                self.notice=fn(self.game.state_data,*args) or 'Saved.'
            except ValueError as exc: self.notice=str(exc)
            else: self.game.persist(); self.game.render()
        if self.parent.winfo_exists(): self.draw()

    def label(self,text,accent=False):
        ttk.Label(self.body,text=text,wraplength=270,justify='left',foreground=ui.MINT if accent else ui.CREAM).pack(fill='x',pady=5)

    def organisation(self,ident,title):
        gang=self.game.state_data.get('job_apps',{}).get('gang') or {}
        if isinstance(ident,str) and gang.get('role')=='Founder' and ident=='crew:'+gang.get('name','').casefold():
            ident=gang
        return organisation_logos.header(self.body,ident,title)

    def button(self,text,fn,*args,enabled=True):
        if self.in_person and fn==jobs.travel: return
        if not self.in_person and self.physical_action(fn,args):
            text='In person · '+text
        ttk.Button(self.body,text=textwrap.fill(text,95 if self.in_person else 34),command=lambda:self.act(fn,*args),
                   state='normal' if enabled and not self.game.busy else 'disabled').pack(fill='x',pady=3)

    def change(self,section):
        self.section=section; self.draw()

    def draw(self):
        for child in self.parent.winfo_children(): child.destroy()
        s=self.game.state_data; d=jobs.ensure(s)
        ttk.Label(self.parent,text='Workplace activities' if self.in_person else 'Bubblegram' if self.criminal else 'Jobseek',font=('Segoe UI',22,'bold')).pack(anchor='w')
        nav=ttk.Frame(self.parent); nav.pack(fill='x',pady=6)
        sections=('Contracts','Leadership','Journal') if self.criminal and self.in_person else ('My career','Development','Journal') if self.in_person else ('Contracts','Network','Journal') if self.criminal else ('Find jobs','My career','Journal')
        for section in sections:
            ttk.Button(nav,text=section,width=10,command=lambda v=section:self.change(v)).pack(side='left',fill='x',expand=True)
        canvas=tk.Canvas(self.parent,bg=ui.PANEL,highlightthickness=0)
        scroll=ttk.Scrollbar(self.parent,command=canvas.yview); scroll.pack(side='right',fill='y')
        canvas.configure(yscrollcommand=scroll.set); canvas.pack(fill='both',expand=True)
        self.body=ttk.Frame(canvas,padding=5); item=canvas.create_window(0,0,window=self.body,anchor='nw')
        self.body.bind('<Configure>',lambda _:canvas.configure(scrollregion=canvas.bbox('all')))
        def fit(event):
            canvas.itemconfigure(item,width=event.width)
            for child in self.body.winfo_children():
                if isinstance(child,ttk.Label): child.configure(wraplength=max(130,event.width-16))
        canvas.bind('<Configure>',fit)
        canvas.bind('<MouseWheel>',lambda e:canvas.yview_scroll(-int(e.delta/120),'units'))
        self.label(town.loop.clock(s))
        if not self.criminal and not self.in_person and self.section!='Find jobs':
            self.label('Work happens in the in-person window. Travel to your employer, finish arriving, then open the workplace. Phone activity buttons open that window without performing the action.')
            ttk.Button(self.body,text='Open workplace in person',command=self.open_workplace).pack(fill='x',pady=3)
        if self.notice: self.label(str(self.notice),True)
        if self.criminal:
            import interpol_ui
            interpol_ui.bubblegram_header(self.body,self.game)
            if self.section in ('Network','My gang'):
                __import__('campaign_ui').phone_directory(self.body,self.game)
        if self.section=='Journal':
            self.label('Private contract journal. No messages or faction identities are shared automatically.' if self.criminal else 'Your employment history and promotion reviews.')
            for event in reversed(d['history'][-80:]):
                if event['private']==self.criminal: self.label(event['text'])
        elif self.section=='Find jobs': self.listings(s,d)
        elif self.section=='My career': self.career(s,d)
        elif self.section in ('Development','Workplace','Projects','Management'): self.development(s,d)
        elif self.section=='Contracts': self.contracts(s,d)
        elif self.section=='Gangs': self.gangs(s,d)
        elif self.section=='My gang': self.my_gang(s,d)
        elif self.section=='Gang icon':
            import gang_icons_ui
            gang_icons_ui.draw(self,s)
        elif self.section=='Reputation': self.reputation(s,d)
        elif self.section=='Leadership': self.leadership(s,d)
        elif self.section=='Hamayashi administration': __import__('post_story_ui').management(self,s)
        else: self.network(s,d)
        phone_theme.apply_tree(self.parent)

    def location(self,venue):
        # Jobseek can advertise an employer's public reception without exposing its affiliation.
        if venue=='site_07_reception': return 'Oculus Winterfield Campus · public reception'
        if venue.endswith('_reception'): return 'Designated '+venue[5:7]+' public reception'
        return town.LOCATIONS[venue]

    def listings(self,s,d):
        self.label('Local employers · one active Jobseek job. Switching retains each ladder. Original protagonist careers stay in Work & ambitions.')
        self.query=ttk.Entry(self.body); self.query.insert(0,self.search); self.query.pack(fill='x')
        def search(): self.search=self.query.get(); self.draw()
        ttk.Button(self.body,text='Search title or workplace',command=search).pack(fill='x',pady=4)
        found=False
        for key,spec in jobs.JOBS.items():
            location=self.location(spec['venue'])
            if self.search.lower() not in (spec['title']+' '+location).lower(): continue
            found=True
            self.label(spec['title'],True)
            self.label(location+f'\n{spec["hours"][0]:02}:00–{spec["hours"][1]:02}:00 · ${spec["pay"]}/hour starting pay\n'+' → '.join(jobs.civilian.titles(key)))
            self.button('Apply · '+spec['title'],jobs.apply,key,enabled=d['employment']!=key)
            self.button('Unsave job' if key in d['saved_jobs'] else 'Save job',jobs.civilian.save_job,key)
        if not found: self.label('No matching careers. Try a workplace or clear the search.')

    def pending(self,s,d,criminal):
        a=d['pending']
        if not a or (a['kind']!='shift')!=criminal: return False
        self.label('Current assignment',True)
        if a['kind']=='shift': self.label(a.get('brief',jobs.JOBS[a['key']]['brief']))
        elif a['kind']=='contract': self.label(a.get('brief', jobs.contract_spec(s,a['key'])['brief']))
        else: self.label('Your sponsor requests a review of a disputed commission. A local supervisor will assess your judgement.')
        self.label(self.location(a['venue'])+f'\n{max(0,a["deadline"]-s["world"]["minute"])} minutes remaining; '+('the decision completes the booked hour.' if a['kind']=='shift' else 'completing work takes 60 minutes.'))
        if not criminal and not self.in_person:
            self.button('Travel / enter workplace',jobs.travel,a['venue'])
            self.label('Resume this shift in the workplace window to choose an approach.')
            self.button('Withdraw · reliability −3',jobs.withdraw)
            return True
        if a['kind']!='shift': self.button('Travel to assignment venue',jobs.travel,a['venue'])
        options=('Focus on craft · craft +4, reliability +1','Support the team · craft +2, reliability +4','Measured pace · craft +1, reliability +2') if not criminal else (
            'Careful approach · 75% pay, reputation +4, heat +2',
            'Standard approach · full pay, reputation +6, heat +8',
            'Reckless approach · reputation +8, heat +20; fails at heat 25+')
        for i,text in enumerate(options): self.button(text,jobs.resolve,i)
        if not criminal:
            self.label('All shifts: professional standing +1. Craft / team / measured choices add service 0 / 3 / 1, leadership 1 / 2 / 1 and team relationship 1 / 3 / 2. Project quality +3 / +2 / +1; specialisation adds +1 quality. Energy cost: 4 / 6 / 9.')
        if criminal: self.label('Failure: no pay, reputation −5. Two failed sponsor assignments suspend sponsorship. Heat falls by 5 each story day.')
        self.button('Withdraw · '+('reputation −2' if criminal else 'reliability −3'),jobs.withdraw)
        return True

    def career(self,s,d):
        self.career_nav()
        if self.pending(s,d,False): return
        key=d['employment']
        if not key: self.label('Find a local job and apply to begin.'); return
        p=jobs.profile(s,key); spec=jobs.JOBS[key]
        self.label(jobs.civilian.titles(key)[p['rank']],True)
        self.label(self.location(spec['venue'])+f'\n${jobs.civilian.wage(key,p)}/hour · {p["shifts"]} shifts\nCraft {p["craft"]} · Reliability {p["reliability"]}\nService {p["service"]} · Leadership {p["leadership"]}\nProfessional standing {p["standing"]}/100 · Earned ${p["earnings"]:,}')
        self.label('One 60-minute Jobseek shift per story day. Complete the decision at work before the hour ends. Calendar conflicts, sleep and travel prevent work.')
        if key=='oculus': self.label('Public reception work only. Employment grants no operational clearance or private affiliations.')
        self.button('Travel / enter workplace',jobs.travel,spec['venue'])
        self.button('Start 60-minute shift',jobs.begin_shift)
        if p['rank']<3:
            shifts,craft,reliability=jobs.LADDER[p['rank']+1]
            self.label(f'Next: {spec["ranks"][p["rank"]+1]}\nReview requires {shifts} shifts, craft {craft}, reliability {reliability}. Each promotion adds $100/hour.')
        elif p['rank']<7:
            shifts,craft,reliability,certs,projects,standing=jobs.civilian.REVIEWS[p['rank']-3]
            self.label(f'Next: {jobs.civilian.titles(key)[p["rank"]+1]}\nRequires {shifts} shifts, craft {craft}, reliability {reliability}, {certs} qualifications, {projects} delivered projects, standing {standing} and a specialisation; leadership {(p["rank"]-2)*12} and morale 50. Promotion adds $100/hour.')
        else: self.label('Career fellowship earned: top of the eight-rank ladder.')
        self.button('Request promotion review',jobs.promote,enabled=p['rank']<7)

    def career_nav(self):
        if self.in_person:
            row=ttk.Frame(self.body); row.pack(fill='x',pady=3)
            for section in ('Development','Workplace','Projects','Management'):
                ttk.Button(row,text=section,command=lambda v=section:self.change(v)).pack(side='left',fill='x',expand=True)
            return
        for section in ('Development','Workplace','Projects','Management'):
            ttk.Button(self.body,text=section,command=lambda v=section:self.change(v)).pack(fill='x',pady=3)

    def development(self,s,d):
        self.career_nav()
        self.label(self.section,True)
        if self.section=='Development':
            self.label('Saved jobs and résumé',True)
            for key in d['saved_jobs']:
                self.label(jobs.JOBS[key]['title'])
                self.button('Apply · '+jobs.JOBS[key]['title'],jobs.apply,key,enabled=key!=d['employment'])
            for key in list(d['jobs']):
                p=jobs.profile(s,key)
                self.label(jobs.JOBS[key]['title']+' · '+jobs.civilian.titles(key)[p['rank']]+f'\n{p["shifts"]} shifts · {len(p["portfolio"])} projects · {len(p["certificates"])} qualifications')
        if not d['employment']:
            self.label('Apply from Find jobs to unlock career development.'); return
        key,p=jobs.civilian.current(s); detail=jobs.civilian.WORKPLACES[key]
        self.label(jobs.JOBS[key]['title']+' · '+self.location(jobs.JOBS[key]['venue']),True)
        self.label('Training, relationship sessions, delivery and management take place at work during opening hours. Travel, sleep, active assignments and calendar commitments block them.')
        self.button('Travel / enter workplace',jobs.travel,jobs.JOBS[key]['venue'])
        if self.section=='Development':
            self.label('Qualifications · three sessions each',True)
            self.label('One paid 30-minute session per story day across employers; each adds 4 to its skill. Qualifications belong to this career and are retained when switching jobs.')
            for course,(title,cost,skill,gain) in jobs.civilian.COURSES.items():
                complete=course in p['certificates']
                self.label(f'{title}: '+('qualified' if complete else f'{p["courses"].get(course,0)}/3 sessions'))
                self.button(f'Train {skill} · ${cost} · 30 minutes',jobs.civilian.train,course,enabled=not complete)
            self.label('Specialisation · rank 3, mentor 20 and matching qualification. Choose once per career; shift pay +$40.',True)
            if p['specialty']:
                self.label(detail[1 if p['specialty']=='expert' else 2]+' · saved specialisation')
            else:
                self.button(detail[1]+' · professional practice qualification; craft shifts add 2 extra craft',jobs.civilian.specialise,'expert')
                self.button(detail[2]+' · client communication qualification; team shifts add 2 extra service',jobs.civilian.specialise,'coordinator')
        elif self.section=='Workplace':
            self.label(detail[3]+' · workplace mentor',True)
            self.label(f'Mentor {p["mentor"]}/100 · Team {p["team"]}/100\nOne 20-minute relationship session per day across employers. Mentor sessions add 10 relationship and 2 craft. Team sessions add 10 relationship and 2 service. These are workplace roles, not personal phone contacts.')
            self.button('Mentoring session · 20 minutes',jobs.civilian.network,'mentor',enabled=p['mentor']<100)
            self.button('Support colleagues · 20 minutes',jobs.civilian.network,'team',enabled=p['team']<100)
            self.label('Mentor 20 unlocks project sponsorship and helps qualify you for specialisation. Career standing is civilian and does not grant criminal reputation or private-site clearance.')
        elif self.section=='Projects':
            self.label(detail[0],True)
            self.label('Unlock at rank 2 with mentor 20. Complete three normal shifts within seven days, then deliver in a 20-minute workplace review. Quality comes from shift choices. Service 12 and team relationship 30 add 1 quality per stage; specialisation adds another 1. Reward: $300 + $30 per quality + $100 per rank; standing +8 and department budget +$200. Closing or missing a project costs 3 standing. Switching jobs preserves the project but does not pause its deadline.')
            item=p['project']
            if item:
                remaining=item['deadline']-s['world']['minute']
                self.label(f'{item["stages"]}/3 stages · Quality {item["quality"]}\n'+(f'{remaining} minutes until deadline' if remaining>=0 else 'Expired · close this project before starting another'),True)
                self.button('Deliver project · 20 minutes' if remaining>=0 else 'Close expired project · standing −3',jobs.civilian.deliver)
                self.button('Abandon project · standing −3',jobs.civilian.deliver,True)
            else: self.button('Accept seven-day project',jobs.civilian.project)
            self.label('Delivered portfolio',True)
            if not p['portfolio']: self.label('No delivered projects yet.')
            for item in reversed(p['portfolio'][-12:]):
                self.label(f'{item["title"]} · Quality {item["quality"]} · ${item["reward"]}')
        else:
            self.label('Department desk · rank 4 and a delivered project',True)
            self.label(f'Department budget ${p["budget"]} · Morale {p["morale"]}/100\nLeadership {p["leadership"]} · Initiatives {p["initiatives"]}')
            self.label('Each initiative takes 30 minutes, costs $100 department budget and adds 3 leadership. One per workplace per day. Project delivery funds this separate budget; personal money is never spent by management.')
            for choice,text in (('quality','Quality review · craft +4'),('team','Team planning · morale +10, reliability +3'),('outreach','Community outreach · standing +4')):
                self.button(text,jobs.civilian.manage,choice,enabled=p['rank']>=3 and bool(p['portfolio'] or p.get('origin_portfolio')))

    def contracts(self,s,d):
        import bubblegram_roles
        if s.get('custom_protagonist'):
            from character_identity import visible
            self.label('Your underworld identity: '+visible(s['custom_protagonist'],context='underworld')['name'],True)
        role = bubblegram_roles.ROLES.get(s['player'])
        if role:
            self.label(role['role'] + '\n' + role['authority'], True)
            self.label('Your established mandate is active. Use commissions or the Leadership desk; no newcomer sponsorship is required. Work is resolved in person at its listed venue.')
            ttk.Button(self.body, text='Open Leadership desk', command=lambda:self.change('Leadership')).pack(fill='x', pady=3)
        self.label(f'{jobs.progression.stage(d)} · Reputation {d["reputation"]}/100 · Heat {d["heat"]}/100',True)
        self.label('Anonymous black-market channel. Aliases are not verified identities. One contract per day; unlock brokers through reputation. Heat 60 blocks new work.')
        if self.pending(s,d,True): return
        for key in jobs.CONTRACTS:
            spec=jobs.contract_spec(s,key)
            if role and spec['faction']: continue
            if spec['faction']:
                self.organisation(spec['faction'],spec['alias']+' · '+spec['title'])
            elif (key=='crew' or spec.get('gang')) and d['gang']:
                self.organisation(d['gang'],spec['alias']+' · '+spec['title'])
            else: self.label(spec['alias']+' · '+spec['title'],True)
            self.label(spec['brief']+f'\n{self.location(spec["venue"])} · ${spec["pay"]} · reputation {spec["rep"]} required')
            if spec.get('rep_cap'): self.label(f'Reputation gains stop at {spec["rep_cap"]}; move to higher-level work to progress.')
            invited=not spec['faction'] or spec['faction'] in d['invitations'] or (d['membership'] or {}).get('faction')==spec['faction']
            if not invited: self.label('Invitation required · build reputation through street and gang work.')
            self.button('Accept · '+spec['title'],jobs.accept,key,enabled=d['reputation']>=spec['rep'] and invited)
        if d['membership']: self.button('Request sponsor assignment',jobs.faction_assignment)

    def network(self,s,d):
        if s['player']=='rei' and s.get('rei_story',{}).get('hamayashi')=='lead':
            ttk.Button(self.body,text='Hamayashi administration',command=lambda:self.change('Hamayashi administration')).pack(fill='x',pady=3)
        for section in ('My gang','Leadership','Gangs','Reputation'):
            ttk.Button(self.body,text=section,command=lambda v=section:self.change(v)).pack(fill='x',pady=3)
        self.label('Established story roles retain their mandate; newcomers progress from street contracts through sponsorship.',True)
        if d.get('established_role'): self.label('Established standing: '+d['established_role']+'. Your story role is retained; you do not start unknown.',True)
        if d.get('leadership'): self.organisation(d['leadership'],('Established operating desk: ' if d['leadership'].get('mission_desk') else 'Large organisation led: ')+d['leadership']['name'])
        if d.get('story_membership'):
            member=d['story_membership']
            self.organisation(member['faction'],member['faction']+' member - '+member['role']+'\n'+member['authority'])
            self.label('Your leadership membership is an established story role; it does not require newcomer sponsorship.',True)
        self.label(f'Reputation {d["reputation"]} · Contracts {d["completed"]} · Heat {d["heat"]}\nConnections: Syndicate {d["connections"]["Syndicate"]}, Shinokami {d["connections"]["Shinokami"]}')
        if not d['gang']:
            self.label('Join or found a gang after 4 contracts and 20 reputation. Any successful contract then adds 1 gang standing.')
            self.button('Join Lantern Crew',jobs.gang)
            self.gang_name=ttk.Entry(self.body); self.gang_name.insert(0,'Night Lanterns'); self.gang_name.pack(fill='x',pady=4)
            ttk.Button(self.body,text='Create named gang',command=lambda:self.act(jobs.gang,self.gang_name.get())).pack(fill='x')
        else: self.organisation(d['gang'],f'{d["gang"]["name"]} · {jobs.progression.gang_title(d["gang"])} · Standing {d["gang"]["standing"]}')
        self.label('Invitations arrive at reputation 40, eight contracts and gang standing 3 with heat below 30. Established large-gang leaders bypass the contract-count requirement. Sponsorship then needs reputation 50 and three faction trials. Choose one faction/branch permanently.')
        for faction,invite in d['invitations'].items():
            self.organisation(faction,invite['alias']+' · '+faction+' · '+invite['status']+'\nYour standing has earned an invitation to broker trials.')
        m=d['membership']
        if m:
            self.organisation(m['faction'],m['faction']+' · '+m['branch']+'\n'+jobs.BRANCHES[m['branch']][2][m['rank']])
            self.label(f'Sponsor {m["sponsor"]}\nSuccessful assignments {m["assignments"]} · Strikes {m["strikes"]}/2')
            if m['faction'] == 'Shinokami':
                self.label('Main contact: Keisuke Hachimura · Pacific Relay Depot. His number and introduction are already in Contacts and Messages. He handles recruits; Takeo’s personal clearance remains separate.',True)
                self.button('Visit Keisuke at Pacific Relay Depot',jobs.travel,'site_02_reception')
                self.label('Second contact: Number Thirteen, commander of US operations. Unlock at Executive (18 successful sponsor assignments, reputation 80, review heat below 30). Suspended sponsorship blocks command contact.')
                import thirteen
                if thirteen.number_allowed(s):
                    self.label('Number Thirteen contact unlocked. Report at Pacific Relay Depot briefing room.',True)
                    self.button('Visit Number Thirteen',jobs.travel,thirteen.HQ)
            self.label('Reviews require heat below 30. Two failures suspend work; rehabilitation requires reputation 50 and heat below 20.')
            for rank,title in enumerate(jobs.BRANCHES[m['branch']][2][1:],1):
                count,rep=jobs.progression.REVIEWS[rank]
                self.label(f'{title}: {count} sponsor assignments · reputation {rep}')
            self.button('Request sponsor assignment',jobs.faction_assignment)
            self.button('Request rank / rehabilitation review',jobs.review)
            if jobs.executive(s):
                self.label(jobs.executive_briefing(s),True)
                self.button('Travel to Syndicate headquarters',jobs.travel,'syndicate_hq')
        for branch,(faction,site,ranks) in jobs.BRANCHES.items():
            self.organisation(faction,branch)
            self.label(' → '.join(ranks))
            if not m and not d.get('syndicate_role'): self.button('Accept invitation · '+branch+' sponsorship',jobs.sponsor,branch,enabled=faction in d['invitations'])
        self.label('Shinokami titles are an authored Japanese ladder for this story. '+jobs.SHINOKAMI_COMMAND)
        self.label('Takeo Mishima, the Human Siege Engine: reputation 100. Meet him in Kestrel Operations Centre’s headquarters briefing room. His number requires Shinokami Regional commander rank or higher in good standing (38 successful sponsor assignments, reputation 95, promotion review with heat below 30). He never leaves headquarters.')
        self.label('Syndicate executive rank unlocks headquarters and a confidential Four Aces identity briefing. Lower ranks and Shinokami membership grant neither. Clearance is personal; outsiders cannot accompany you or hear the briefing. Affiliate briefing-room and protected-research permissions remain separate. Jokers and the Cardmaster remain story roles.')

    def gangs(self,s,d):
        self.label('Gang directory · membership is private',True)
        if d['gang']:
            self.organisation(d['gang'],d['gang']['name']+' · '+jobs.progression.gang_title(d['gang'])+f'\nStanding {d["gang"]["standing"]}')
            self.button('Request gang advancement',jobs.progression.review_gang)
            self.button('Leave gang · preserves past affiliations',jobs.progression.leave)
        self.label('Gang reviews: standing 3 / 8 / 16 and reputation 30 / 45 / 65. Founders grow from a small crew into a city network; members advance to captain. Sponsored members cannot switch gangs.')
        for key,spec in jobs.progression.GANGS.items():
            self.organisation(key,spec['name'])
            import gang_leaders
            leader=gang_leaders.LEADERS[key]
            self.label(leader['name']+' · '+leader['role']+'\nLives at '+leader['title'])
            self.button('Visit '+leader['title'],jobs.travel,leader['base'])
            self.label(spec['kind']+f'\nJoin: reputation {spec["rep"]}, {spec["jobs"]} contracts.')
            self.button('Join '+spec['name'],jobs.progression.join,key,enabled=not d['gang'])
            if (d['gang'] or {}).get('id')==key:
                self.label('Leader’s direct number and introduction are saved in Contacts and Messages.')
                ttk.Button(self.body,text='Message '+leader['name'],command=lambda n=leader['name']:self.phone.open_thread('npc:'+n,True)).pack(fill='x',pady=3)
            if key=='hamayashi':
                self.label('Rei does not know this successor exists until he sees evidence. Revealing your present or past affiliation costs 40 trust and 30 closeness once; simply leaving will not erase it.')
                self.button('Investigate successor evidence' if s['player']=='rei' else 'Show Rei evidence in person · reveal any affiliation',jobs.progression.reveal_hamayashi)
        self.label('To found your own crew, return to Network. Existing organisation names cannot be claimed.')

    def my_gang(self,s,d):
        import custom_gangs as cg
        self.label('My gang · recruitment and management',True)
        self.label('Potential recruits are ordinary adult residents who may choose to join after you build trust. They keep their existing jobs and routines. No prior criminal history is implied.')
        try: g=cg.crew(s)
        except ValueError:
            self.label('Found a named gang in Network: 20 reputation and four completed contracts. The recruit directory below lets you plan ahead.')
            g=None
        if g:
            self.organisation(g,g['name'])
            ttk.Button(self.body,text='Create or edit gang icon',command=lambda:self.change('Gang icon')).pack(fill='x',pady=3)
            self.label(f'{g["name"]} · {len(g["members"])}/{cg.capacity(g)} members · '+g['charter'],True)
            self.label('Capacity starts at 3 and grows by 2 per gang rank. Each officer role has one holder; Member has no limit. Bonuses apply to crew, network and leadership contracts, not faction assignments.')
            entry=ttk.Entry(self.body); entry.insert(0,g['charter']); entry.pack(fill='x')
            ttk.Button(self.body,text='Save charter',command=lambda:self.act(cg.charter,entry.get())).pack(fill='x',pady=3)
            for role,detail in cg.ROLES.items(): self.label(role+' · '+detail)
            for name,member in list(g['members'].items()):
                self.label(name+' · '+member['role'],True)
                choice=ttk.Combobox(self.body,values=list(cg.ROLES),state='readonly'); choice.set(member['role']); choice.pack(fill='x')
                ttk.Button(self.body,text='Assign role',command=lambda n=name,c=choice:self.act(cg.assign,n,c.get())).pack(fill='x',pady=3)
                self.button('Remove from roster · '+name,cg.dismiss,name)
            self.label('Assimilation offers',True)
            self.label('Syndicate notices you at reputation 60; Shinokami at 70. Declining has no penalty and is final for this crew. Accepting preserves your gang name and roster but binds you to one faction at probation. Normal sponsorship requirements apply: invitation, reputation 50, three faction trials, standing 3, heat below 30, and no unresolved diplomacy. No command clearance is granted.')
            for faction,offer in g['assimilation'].items():
                self.label(faction+' · '+offer['status'],True)
                if offer['status']=='offered' and not d['membership']:
                    for branch,spec in jobs.BRANCHES.items():
                        if spec[0]==faction: self.button('Accept assimilation · '+branch,cg.respond,faction,True,branch)
                    self.button('Decline · remain independent',cg.respond,faction)
            if g.get('parent_faction'): self.label('Assimilated affiliate of '+g['parent_faction'])
            ttk.Button(self.body,text='Organisation relations and meetings',command=lambda:self.change('Leadership')).pack(fill='x',pady=3)
        self.label('Recruit directory',True)
        for name,(role,rep,trust) in cg.RECRUITS.items():
            venue=cg.location(s,name)
            person=cg.town_residents.RESIDENTS[name]
            self.label(name+f' · Age {person["age"]} · '+person['role']+f'\nSuggested role: {role} · Reputation {rep} · Trust {trust}\n'+('Currently at '+self.location(venue) if venue else 'Off duty · public routine 08:00–22:00'),True)
            if name in cg.street_recruits.RESIDENTS: self.label(person['life'])
            self.label(cg.reason(s,name) or 'Ready to discuss recruitment in person.' if g else 'Found your gang to recruit.')
            if venue: self.button('Travel to '+name,jobs.travel,venue)
            if g and name not in g['members']:
                ttk.Button(self.body,text='Discuss recruitment in person',command=lambda n=name:self.open_recruit(n)).pack(fill='x',pady=3)

    def open_recruit(self,name):
        from custom_gangs_ui import open_recruit
        try: open_recruit(self.game,name)
        except ValueError as exc:
            self.notice=str(exc); self.draw()

    def reputation(self,s,d):
        self.label(jobs.progression.stage(d)+f' · {d["reputation"]}/100',True)
        self.label(' → '.join(f'{label} ({minimum})' for minimum,label in jobs.progression.STAGES))
        self.label('Criminal-world reputations · operational names only. Standing does not reveal a civilian identity, grant contacts or establish a meeting.')
        for row in jobs.progression.directory(s): self.label(row)
        self.label('Garrett and Ivan retain large-organisation leadership. The Aces appear under their suit titles until the player has earned the existing identity clearance.')

    def leadership(self,s,d):
        import syndicate_council
        syndicate_council.ensure(s)
        if syndicate_council.eligible(s):
            self.label('Face-card council · Sundays 20:00–21:00', True)
            self.label('The Crow chairs the weekly council at headquarters. Open Calendar to join; stay for 45 game minutes. ' +
                       ('Attendance is mandatory for Ivan.' if s['player']=='ivan' else 'Reserved for Jack and above.'))
        import crime_diplomacy as dip
        from careers_ui import stamp
        self.label('Leadership desk',True)
        role=dip.mandate(s)
        if not role:
            self.label('Unlock by founding your own gang, reaching gang Captain, or becoming a Syndicate or Shinokami executive. Garrett and Ivan already lead large organisations. Suspended faction sponsorship must be restored first.')
            return
        b=dip.ensure(s)
        import bubblegram_roles
        canonical = bubblegram_roles.ROLES.get(s['player'])
        if canonical:
            self.label(canonical['role']+'\n'+canonical['authority'], True)
            self.label('This is your private operating desk. Mission authority does not transfer command of a Suit or grant access to unrelated organisations. Reputation, heat, meetings and treasury are saved separately for this playthrough.')
        if s['player']=='ivan': self.label('Syndicate member · Black and White Joker\nLeader · Black and White Joker network',True)
        self.organisation(role[0],role[1]+' · '+role[2])
        if s['player']=='garrett':
            self.label(f'Red Dragons member and leader · Standing {dip.relation(b,"dragons")}/100',True)
            import gang_members
            self.label('Established working relationships',True)
            for name in gang_members.coworkers(s):
                connection=s['npc_chats'][name]['connection']
                self.label(name+' · '+gang_members.MEMBERS[name]['role']+
                           f'\n{connection["status"].title()} · Trust {connection["trust"]}/100 · Closeness {connection["closeness"]}/100')
                ttk.Button(self.body,text='Message '+name,command=lambda n=name:self.phone.open_thread('npc:'+n,True)).pack(fill='x',pady=3)
        self.label(f'Organisation funds ${b["treasury"]:,} · Influence {b["influence"]}/100\nPersonal funds ${s["world"]["money"]:,}')
        self.label('Your organisation has a separate, one-time operating reserve. Deal capital comes from this reserve; successful deals pay you 20% of profit. Two deals may be active at once. Your criminal daily-operation limit applies to deal completion. Heat 60 blocks new business and deal completion.')
        self.button('Add $1,000 from personal funds',dip.fund)
        self.label('Scheduled in-person meetings · arrive within 15 minutes. Review three ten-minute agenda items, then decide before the hour ends. Relationships 50, influence 10 and reputation 80 unlock senior-level negotiations. Headquarters clearance remains required.')
        self.label('Incoming invitations',True)
        for i in b['invitations'][-10:]:
            if i['status']!='offered': continue
            spec=dip.ORGANISATIONS[i['target']]
            self.organisation(i['target'],spec[3 if i['leader'] else 2]+' invites you.\n'+stamp(i['start']))
            self.button('Accept invitation',dip.invitation,i['id'])
            self.button('Accept for the following day',dip.invitation,i['id'],True,1)
            self.button('Decline · no penalty',dip.invitation,i['id'],False)
        self.label('Meetings and negotiations',True)
        for m in b['meetings'][-12:]:
            self.organisation(m['target'],m['representative']+' · '+m['status']+'\n'+stamp(m['start'])+' · '+self.location(m['venue']))
            if m['status'] not in ('booked','in_progress'): continue
            self.label('Agenda: '+'; '.join(m['agenda'])+'\nEnds '+stamp(m['end']))
            self.button('Travel to meeting',jobs.travel,m['venue'])
            self.button('Wait until meeting · up to two days',dip.wait,m['id'])
            ttk.Button(self.body,text='Open meeting in person',command=lambda ident=m['id']:self.open_meeting(ident)).pack(fill='x',pady=3)
            self.button('Move meeting one day later',dip.reschedule,m['id'])
            self.button('Cancel meeting · late cancellation costs relationship 3',dip.cancel,m['id'])
        self.label('Active deals',True)
        self.label('Deals are due in three days. A missed deadline loses committed capital, relationship 10 and reputation 3. You can extend once or abandon for half your capital back.')
        for deal in b['deals'][-12:]:
            self.organisation(deal['target'],dip.ORGANISATIONS[deal['target']][0]+' · '+deal['status']+'\nDue '+stamp(deal['deadline']))
            if deal['status']!='active': continue
            self.button('Travel to deal appointment',jobs.travel,deal['venue'])
            self.button('Complete deal · 60 minutes',dip.settle,deal['id'])
            self.button('Extend one day · relationship −2',dip.extend,deal['id'],enabled=not deal['extended'])
            self.button('Abandon · recover half capital, relationship −6',dip.abandon,deal['id'])
        self.label('Other organisations',True)
        self.label('Request one meeting per day for 18:00 tomorrow. Named leaders receive you at their bases in the in-person window. Joining a gang supplies its leader’s direct contact. Meetings do not bypass the Crow’s or Takeo’s personal-number gates.')
        for key,spec in dip.ORGANISATIONS.items():
            if key==role[0]: continue
            self.organisation(key,spec[0]+f' · Relationship {dip.relation(b,key)}/100')
            if key=='hamayashi': self.label('Agreeing to a deal establishes a business affiliation. Rei can discover it through the existing evidence action.')
            self.button('Request meeting · '+spec[2],dip.request,key,enabled=dip.access(s,key))
            self.button('Request senior negotiation · '+spec[2],dip.request,key,True,enabled=dip.access(s,key) and dip.leader_ready(s,b,key))
            if not dip.access(s,key): self.label('Headquarters clearance required before this appointment can be booked.')
        self.label('Leadership journal',True)
        for item in reversed(b['history'][-12:]): self.label(item['text'])

    def open_meeting(self,ident):
        if self.game.busy: return
        import crime_diplomacy
        try: gid=crime_diplomacy.begin(self.game.state_data,ident)
        except ValueError as exc:
            self.notice=str(exc); self.draw(); return
        self.game.persist(); self.game.select_group(gid); self.game.show_in_person()


def show(phone,frame,criminal=False):
    phone.job_board=JobBoard(phone,frame,criminal)

