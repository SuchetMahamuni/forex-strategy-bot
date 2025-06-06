class universal:
    colour_theme = ('yellow', 'cyan')

    market_watch_labels = {}
    
    instruments = [
            'US30',
            'US100',
            'EURUSD',
            'XAUUSD',
            'USDJPY',
            'US500',
        ]
    instruments_sml = [
            'EURUSD.sml',
            'XAUUSD.sml',
            'USDJPY.sml',
        ]
    # items: account_info[1], Queues[2], add_instrument[4], trading[{'process':'', 'Queues':''},{...},{...},{...},]
    processes = {'account_info':[],
                 'Queues':[],
                 'add_instrument':[],
                 'trading':[]
                 }
    app_working = True


class LoadingSpinner:
    def __init__(self, parent, size=60, dot_count=5, dot_sizes = [1.9, 2.4, 2.9, 3.4, 3.9], bg = '#242424', gap = 1):
        self.canvas = tk.Canvas(parent, width=size, height=size, highlightthickness=0, bg=bg)
        self.size = size
        self.dot_count = dot_count
        self.dots = []
        self.dot_sizes = dot_sizes  # Sizes for the dots
        self.angle = 0
        self.running = False
        
        # Create dots
        self._create_dots(gap)

    def _create_dots(self, gap):
        """Initialize dots in a closely spaced pattern."""
        radius = (self.size / 2) - max(self.dot_sizes)  # Radius for the dots to move along
        center_x = self.size / 2
        center_y = self.size / 2

        for i, dot_radius in enumerate(self.dot_sizes):
            # Adjust angle offset to space dots closely together
            self.angle_offset = (2 * math.pi / (self.dot_count * 4)) * i * gap
            x = center_x + radius * math.cos(self.angle_offset)
            y = center_y + radius * math.sin(self.angle_offset)
            dot = self.canvas.create_oval(x - dot_radius, y - dot_radius,
                                          x + dot_radius, y + dot_radius,
                                          fill='grey')
            self.dots.append((dot, self.angle_offset))

    def start(self):
        self.running = True
        self._rotate()

    def stop(self):
        self.running = False

    def _rotate(self):
        """Animate the dots to rotate in a circle."""
        if not self.running:
            return

        self.angle = (self.angle + 6) % 360
        center_x = self.size / 2
        center_y = self.size / 2
        radius = (self.size / 2) - max(self.dot_sizes)

        for i, (dot, angle_offset) in enumerate(self.dots):
            angle = math.radians(self.angle) + angle_offset
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            dot_radius = self.dot_sizes[i]
            self.canvas.coords(dot, x - dot_radius, y - dot_radius,
                               x + dot_radius, y + dot_radius)

        self.canvas.after(10, self._rotate)  # Call this method again after 50 milliseconds

    def pack(self, **kwargs):
        self.canvas.pack(**kwargs)

    def pack_forget(self, **kwargs):
        self.canvas.pack_forget(**kwargs)

def CTkWindowSeparator(master, colour, size = 2, length = 75, multiply = 200, orientation = "Horizontal"):
    SetColour = colour
    LineLength = length/100 * multiply
    if orientation == "Horizontal":
        Separator = ctk.CTkProgressBar(master=master, height=size, width=LineLength)
    else:
        Separator = ctk.CTkProgressBar(master=master, width=size, height=LineLength)

    Separator.configure(progress_color=SetColour, fg_color=SetColour)
    return Separator


class widgets:
    def __init__(self):
        self.strategy = ctk.CTkToplevel()
        self.strategy.title("New strategy")
        self.strategy.geometry("470x400")

        ctk.CTkLabel(self.strategy, text='Strategy : ', font = ('Ebrima',12), justify='right').grid(row=0, column=0, padx=10, pady=5, sticky='w')

        # Strategy select dropdown
        self.strategy_options = ctk.CTkComboBox(self.strategy, values = list(universal.strategies.keys()), border_color = universal.colour_theme, width = 280, font = ('Arial',14))
        self.strategy_options.grid(row=0, column=1, padx=10, pady=(10,5))
        self.strategy_options.set(list(universal.strategies.keys())[0])
        
        # Strategy on which instruments
        ctk.CTkLabel(self.strategy, text='Instrument: ', font = ('Ebrima',12), justify='right').grid(row=1, column=0, padx=10, pady=5, sticky='w')

        # Instrument select dropdown
        self.instrument_options = ctk.CTkComboBox(self.strategy, values = universal.instruments, border_color = universal.colour_theme, width = 280, font = ('Arial',14))
        self.instrument_options.grid(row=1, column=1, padx=10, pady=5,)
        self.instrument_options.set(universal.instruments[0])

        # Strategy on which timeframe
        ctk.CTkLabel(self.strategy, text='Timeframe: ', font = ('Ebrima',12), justify='right').grid(row=2, column=0, padx=10, pady=5, sticky='w')

        # Timeframe select dropdown
        self.timeframe_options = ctk.CTkComboBox(self.strategy, values = list(comm.Timeframes.keys()), border_color = universal.colour_theme, width = 280, font = ('Arial',14))
        self.timeframe_options.grid(row=2, column=1, padx=10, pady=5,)
        self.timeframe_options.set(list(comm.Timeframes.keys())[4])

        # Action options
        ctk.CTkLabel(self.strategy, text='Action : ', font = ('Ebrima',12), justify='right').grid(row=3, column=0, padx=10, pady=10, sticky='w')

        # Action select checkbox
        self.action = ctk.StringVar(value = False)
        text = ctk.StringVar(value = "   Only notify")
        self.checkbox = ctk.CTkCheckBox(self.strategy, variable = self.action, onvalue = True, offvalue = False,text=text.get(), command = self.checkbox_event) 
        self.checkbox.grid(row=3, column=1, padx=10, pady=10, sticky = 'w')

        # Target profit
        ctk.CTkLabel(self.strategy, text='Units (USD) : ', font = ('Ebrima',12), justify='right').grid(row=4, column=0, padx=10, pady=10, sticky='w')

        self.trade_volume = ctk.CTkEntry(master=self.strategy, placeholder_text = "Ex. 10, 1, 0.01, etc.", width = 280, border_color = universal.colour_theme, font = ('Arial',14))
        self.trade_volume.grid(row=4, column=1, padx=10, pady=10, sticky = 'w')

        # Units(USD)
        ctk.CTkLabel(self.strategy, text='Target Profit (Pips) : ', font = ('Ebrima',12), justify='right').grid(row=5, column=0, padx=10, pady=10, sticky='w')

        self.target_pips = ctk.CTkEntry(master=self.strategy, placeholder_text = "Ex. 100, 0.01, 40, etc.", width = 280, border_color = universal.colour_theme, font = ('Arial',14))
        self.target_pips.grid(row=5, column=1, padx=10, pady=10, sticky = 'w')

        # Advanced options button
        self.advanced_options_button = ctk.CTkButton(master = self.strategy,command= self.Advanced_options_window,text= "Advanced Options",font= ('Helvetica', 14),
            text_color="white", hover = False, hover_color= "black",height = 25,border_width=0, corner_radius=1,
            border_color= "#d3d3d3", bg_color="#262626", fg_color= "#262626")
        self.advanced_options_button.grid(row = 6, column = 1, padx = 20, pady = 10, sticky = 'ew')

        # Submit button
        self.Submit = ctk.CTkButton(self.strategy, text = "Submit", font = ('Ebrima',16), command = self.submit_action)#lambda: self.Analyze(self.options_dropdown_var.get()))
        self.Submit.grid(row = 8, column = 0, columnspan = 2, padx = 20, pady = 20, sticky = 'ew')

        self.strategy.attributes('-topmost', True)
        self.set_adv_values(Set=False)
        self.name = None

    def submit_action(self):
        # Add to window processes_frame
        new_process = ctk.CTkFrame(master=processes_frame, height = 20, width = float(root.winfo_width() * 0.779))
        close_process_button = ctk.CTkButton(new_process, text = 'x', corner_radius = 2, width = 15, height = 3, font = ('Bold',10),)
        process_label = ctk.CTkLabel(new_process, text='')
        
        if len(universal.processes['trading']) == 0:
            new_process.grid(row = len(universal.processes['trading']), padx=4, pady=(5,2))
        else:
            new_process.grid(row = len(universal.processes['trading']), padx=4, pady=2)
        
        
        # New process
        details = {
            'strategy': self.strategy_options.get(),
            'instrument': self.instrument_options.get(),
            'timeframe': self.timeframe_options.get(),
            'action': bool(int(self.action.get())),
            'Units' : float(self.trade_volume.get()),
            'Increment': self.increment,
            'target pips': float(self.target_pips.get()),
            'expiration time': (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%d/%m/%Y 02:29:55'),
            'Spreads': [self.buy_spread, self.sell_spread],
            'seconds_input':self.seconds_input}
        
        S_queue = mp.Queue()
        A_queue = mp.Queue()
        strategy_process = mp.Process(target=function_strategy, args=(S_queue, A_queue, details, universal.credentials,))
        strategy_process.start()
        process_id = calendar.timegm(datetime.datetime.today().utctimetuple())
        universal.processes['trading'].append({
                    'process': strategy_process,
                    'process_id': process_id,
                    'Queues': [S_queue, A_queue],# S - strategy working, A - action (only notify or execute order)
                    'Details': details,
                    'S value': True,
                    'A value': details['action'], # Changeable...
                    'window' : [new_process, close_process_button, process_label]
            })

        # Permanent
        self.strategy.destroy()
        # process id, instrument, action, strategy
        text = f"{universal.processes['trading'][-1]['process_id']}\t\t\t\t{details['instrument'].split('.')[0]}\t\t\t\t{'Only notify' if not details['action'] else 'Execute Orders'}\t\t\t\t{details['strategy']}"
        close_process_button.pack(side="right", padx=(0,5))
        close_process_button.configure(command=lambda : shutdown_process(process_id))
        process_label.configure(text=text, font = ('Ebrima',12), width = float(root.winfo_width() * 0.76), justify='left', anchor='w')
        process_label.pack(side='left', anchor='w', padx=(0,10))
        process_label.bind("<Double-Button-1>", lambda _: self.handler(process_id))
        tooltip = ToolTip(close_process_button, "Terminate Process", place='left')
        

    def checkbox_event(self):
        if self.action.get() == '1':
            self.checkbox.configure(text = "Execute orders")
        else:
            self.checkbox.configure(text = "   Only notify")

    def handler(self, process_id):
        for i in range(0, len(universal.processes['trading'])):
            if process_id == universal.processes['trading'][i]['process_id']:
                break
        edit_strategy = new_process_window()

        edit_strategy.strategy.title("Edit strategy")
        edit_strategy.strategy_options.set(universal.processes['trading'][i]['Details']['strategy'])
        edit_strategy.strategy_options.configure(state='disabled')

        edit_strategy.instrument_options.set(universal.processes['trading'][i]['Details']['instrument'])
        edit_strategy.instrument_options.configure(state='disabled')

        edit_strategy.timeframe_options.set(universal.processes['trading'][i]['Details']['timeframe'])
        edit_strategy.timeframe_options.configure(state='disabled')

        if universal.processes['trading'][i]['Details']['action']:
            edit_strategy.checkbox.select()
        else:
            edit_strategy.checkbox.deselect()

        edit_strategy.trade_volume.insert(0,universal.processes['trading'][i]['Details']['Units'])
        edit_strategy.target_pips.insert(0,universal.processes['trading'][i]['Details']['target pips'])

        edit_strategy.Submit.configure(text = 'Modify',
                                       command=lambda : self.edit_action(edit_strategy, i, edit_strategy.action.get(), edit_strategy.trade_volume.get(), edit_strategy.target_pips.get()))

        edit_strategy.checkbox_event()

        edit_strategy.increment = universal.processes['trading'][i]['Details']['Increment']
        edit_strategy.buy_spread = universal.processes['trading'][i]['Details']['Spreads'][0]
        edit_strategy.sell_spread = universal.processes['trading'][i]['Details']['Spreads'][1]
        edit_strategy.seconds_input = universal.processes['trading'][i]['Details']['seconds_input']        

    def edit_action(self, window, index, action_, trade_volume, target_pips):
        window.strategy.destroy()
        #print([self.buy_spread, self.sell_spread])
        universal.processes['trading'][index]['Details']['action'] = bool(int(action_))
        universal.processes['trading'][index]['A value'] = bool(int(action_))
        universal.processes['trading'][index]['Details']['Units'] = float(trade_volume)
        universal.processes['trading'][index]['Details']['target pips'] = float(target_pips)
        universal.processes['trading'][index]['Details']['Spreads'] = [window.buy_spread, window.sell_spread]
        universal.processes['trading'][index]['Details']['Increment'] = window.increment
        universal.processes['trading'][index]['Details']['seconds_input'] = window.seconds_input

        text = f"{universal.processes['trading'][index]['process_id']}\t\t\t\t{universal.processes['trading'][index]['Details']['instrument'].split('.')[0]}\t\t\t\t{'Only notify' if not universal.processes['trading'][index]['Details']['action'] else 'Execute Orders'}\t\t\t\t{universal.processes['trading'][index]['Details']['strategy']}"
        universal.processes['trading'][index]['window'][2].configure(text=text)

    def Advanced_options_window(self):
        self.adv_window = ctk.CTkToplevel()
        self.adv_window.title("Advanced Options")
        self.adv_window.geometry("470x400+700+100")

        # Increment with 'x' units
        ctk.CTkLabel(self.adv_window, text='Increment units with : ', font = ('Ebrima',12), ).grid(row=0, column=0, padx=15, pady = 15, sticky='w')
        self.adv_increment = ctk.CTkComboBox(self.adv_window, values = ['No increment','Same increment','1','2','3'],
                                             border_color = universal.colour_theme, width = 280, font = ('Arial',14))
        #self.adv_increment = ctk.CTkEntry(master=self.adv_window, placeholder_text = "Ex. 1,2.5,3", width = 80, border_color = universal.colour_theme, font = ('Arial',14))
        self.adv_increment.grid(row=0, column=1, padx=20, pady=15, sticky='w')
        self.adv_increment.set(self.increment)

        # Spread
        CTkWindowSeparator(self.adv_window, 'Grey', length = 450, multiply = 90).grid(row=1,column=0, columnspan = 3, padx = (10,0), pady = 10)
        ctk.CTkLabel(self.adv_window, text=' Spreads ').grid(row=1, column=0, padx=20, sticky='w')

        # Buy spread
        ctk.CTkLabel(self.adv_window, text='Buy spread : ', font = ('Ebrima',12), ).grid(row=2, column=0, padx=15, sticky='w')
        self.adv_buy_spread = ctk.CTkEntry(master=self.adv_window, placeholder_text = "Ex. 1,2,3", width = 80, border_color = universal.colour_theme, font = ('Arial',14))
        self.adv_buy_spread.grid(row=2, column=1, padx=20, sticky='w')
        self.adv_buy_spread.insert(0, self.buy_spread)

        # Sell spread
        ctk.CTkLabel(self.adv_window, text='Sell spread : ', font = ('Ebrima',12), ).grid(row=3, column=0, padx=15, pady = 10, sticky='w')
        self.adv_sell_spread = ctk.CTkEntry(master=self.adv_window, placeholder_text = "Ex. 1,2,3", width = 80, border_color = universal.colour_theme, font = ('Arial',14))
        self.adv_sell_spread.grid(row=3, column=1, padx=20, pady = 10, sticky='w')
        self.adv_sell_spread.insert(0, self.sell_spread)

        # Seconds delay update
        ctk.CTkLabel(self.adv_window, text='Seconds delay update : ', font = ('Ebrima',12), ).grid(row=4, column=0, padx=15, pady = 10, sticky='w')
        self.adv_seconds_input = ctk.CTkEntry(master=self.adv_window, placeholder_text = "Ex. 1,2,3", width = 80, border_color = universal.colour_theme, font = ('Arial',14))
        self.adv_seconds_input.grid(row=4, column=1, padx=20, pady = 10, sticky='w')
        self.adv_seconds_input.insert(0, self.seconds_input)

        ok_button = ctk.CTkButton(self.adv_window, text = " Set ", font = ('Ebrima',16), command = self.set_adv_values)
        ok_button.grid(row = 6, column = 0, columnspan = 3, padx = 10, pady = 10)

        self.adv_window.attributes('-topmost', True)

    def set_adv_values(self, Set = True):
        if Set:
            self.buy_spread = self.adv_buy_spread.get()
            self.sell_spread = self.adv_sell_spread.get()
            self.increment =  self.adv_increment.get()
            self.seconds_input =  self.adv_seconds_input.get()

            self.adv_window.destroy()

        else:
            self.buy_spread = 0
            self.sell_spread = 0
            self.seconds_input = 15
            self.increment = 'Same increment'
        print(self.seconds_input)

    def add_template(self, name):
        global my_templates, delete_templates
        # Add template to database and then to menu bar also
        details = {
            'strategy': self.strategy_options.get(),
            'instrument': self.instrument_options.get(),
            'timeframe': self.timeframe_options.get(),
            'action': bool(int(self.action.get())),
            'Units' : float(self.trade_volume.get()),
            'Increment': self.increment,
            'target pips': float(self.target_pips.get()),
            'expiration time': (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%d/%m/%Y 02:29:55'),
            'Spreads': [self.buy_spread, self.sell_spread],
            'seconds_input': self.seconds_input }

        print(f"""INSERT INTO templates VALUES('{name}', '{json.dumps(details)}');""")
        comm.cursor.execute(f"""INSERT INTO templates VALUES('{name}', '{json.dumps(details)}');""")
        comm.db.commit()

        my_templates.add_option(option = name, command = lambda: load_template(details))
        delete_templates.add_option(option = name, command = lambda: load_template(details))
        self.strategy.destroy()

def shutdown_process(process_id):
    x = (False,0)
    for i in range(0, len(universal.processes['trading'])):
        if process_id == universal.processes['trading'][i]['process_id']:
            universal.processes['trading'][i]['S value'] = False
            universal.processes['trading'][i]['window'][0].grid_forget()
            universal.processes['trading'][i]['process'].kill()
            x = (True, i)
    if x[0]:
        del universal.processes['trading'][x[1]]
    else:
        pass


def process_manager():
    while universal.app_working:
        time.sleep(0.7)
        for i in range(0, len(universal.processes['trading'])):
            universal.processes['trading'][i]['Queues'][0].put(universal.processes['trading'][i]['S value'])
            universal.processes['trading'][i]['Queues'][1].put([ universal.processes['trading'][i]['A value'],
                                                                 universal.processes['trading'][i]['Details']['Units'],
                                                                 universal.processes['trading'][i]['Details']['target pips'],
                                                                 universal.processes['trading'][i]['Details']['Spreads'],
                                                                 universal.processes['trading'][i]['Details']['Increment'],
                                                                 universal.processes['trading'][i]['Details']['seconds_input']     ])
            

def function_strategy(queue, a_queue, details, creds):
    # To notify..... Tickets 0 -> order, 1 -> position
    global first_time, tickets, strategy
    tickets = {'order' : None, 'position' : None, 'position open price':None}
    toaster = WindowsToaster("Live Trading")

    strategy = universal.strategies[details['strategy']]
    strategy = strategy(details, creds[0],creds[1],creds[2])

    modify_permission = details['action']
    lot = details['Units']
    Total_Loss = 0
    current_trade_max_loss = 0
    comment = ''
    order_bs = None
    order_position = [False,False]      # 0 -> position closed, 1 -> order executed (order becomes position)
    while True:
        expiration_time = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%d/%m/%Y 05:29:55')
        # Check if have to close process
        if not queue.get():
            break

        variable_details = a_queue.get()    # A value, lot, target pips, Spreads, increment(same, no, number), Seconds input
        modify_permission = True if variable_details[0] else modify_permission

        # Check for open position
        if tickets['position'] is not None:
            request = strategy.update_position(tickets['position'], spreads = variable_details[3])

            if int(time.strftime("%S")) % int(variable_details[5]) == 0:
                success, comment = strategy.comm.modify_position(request)
                
                if comment == "Invalid request":
                    order_position[0] = True

                elif not success and comment == "Invalid stops":
                    position_volume, open_price, position_type,sl = strategy.comm.history_position_details(tickets['position'], [14, 19, 6,17])
                    close_price = strategy.comm.history_position_details(tickets['order'], [19])
                    
                    if position_type == strategy.comm.mt5.ORDER_TYPE_BUY_STOP:
                        current_trade_max_loss = (float(open_price) - float(close_price)) * float(position_volume) + Total_Loss   # Change
                    else:
                        current_trade_max_loss = (float(close_price) - float(open_price)) * float(position_volume) + Total_Loss
                    print('Ticket:', tickets['position'], '\tOpen:',open_price, '\tStop loss:', sl, '\tlot:',position_volume, '\tmax loss:', current_trade_max_loss)
                    
                    
                else:
                    position_volume, open_price, position_type = strategy.comm.history_position_details(tickets['position'], [14, 19, 6])
                    if position_type == strategy.comm.mt5.ORDER_TYPE_BUY_STOP:
                        current_trade_max_loss = (float(tickets['position open price']) - float(request['sl'])) * float(position_volume) + Total_Loss
                    else:
                        current_trade_max_loss = (float(request['sl']) - float(tickets['position open price'])) * float(position_volume) + Total_Loss
                    print('Ticket:', tickets['position'], '\tOpen:',tickets['position open price'], '\tStop loss:', request['sl'], '\tlot:',position_volume, '\tmax loss:', current_trade_max_loss,' Total loss',Total_Loss)
        else:
            pass

        # Modify order
        if tickets['order'] is not None:

            # Delete order
            if lot != variable_details[1]:
                lot = variable_details[1]
                request = strategy.update_order(tickets['order'], variable_details[1], variable_details[2])
                strategy.comm.delete_order(tickets['order'])
                order_bs = request['type']
                tickets['order'] = None
            # Update order
            else:
                request = strategy.update_order(tickets['order'], variable_details[1], variable_details[2], spreads = variable_details[3], volume = variable_details[4], total_loss = current_trade_max_loss)
                if request == 0:
                    continue
                if modify_permission:
                    # if time is == second
                    if int(time.strftime("%S")) % int(variable_details[5]) == 0:
                        success, comment = strategy.comm.modify_order(request)
                        # Code to be put inside 
                        if comment == 'Invalid request':
                            position_ticket = tickets['position']
                            tickets['position'] = tickets['order']
                            tickets['order'] = None
                            tickets['position open price'] = request['price']
                            
                            # it means position_ticket closed in loss, So we have to increment units by 1
                            strategy.units += 1
                            
                            order_bs = tickets['position']
                            print('Units incremented')

                            # Check out for position also
                            if position_ticket is not None:
                                request = strategy.update_position(position_ticket, spreads = variable_details[3])
                                success, comment = strategy.comm.modify_position(request)
                                if comment == "Invalid request":
                                    order_position[0] = True
                                    Total_Loss = current_trade_max_loss
                            
                            order_position[1] = True

                        elif comment == 'Invalid price':
                            pass
                        else:
                            pass
                else:
                    pass

        # New order
        else:
            current_position = strategy.past_to_now_position() if order_bs is None else order_bs
            order_bs = None
            request,order = strategy.signal_position(current_position, variable_details[1], variable_details[2], expiration_time, spreads = variable_details[3], volume = variable_details[4])
            result = strategy.comm.pending_orders(request)
            if result != False:
                tickets['order'] = result[2]
            else:
                pass

        
        # Take profit triggered
        if order_position[0] and not order_position[1]:    
            strategy.units = 1

            Total_Loss = 0
            current_trade_max_loss = 0

            # Delete order
            try:
                request = strategy.update_order(tickets['order'], variable_details[1], variable_details[2])
                strategy.comm.delete_order(tickets['order'])
            except sqlite3.OperationalError:
                pass
            finally:
                order_bs = request['type']
                tickets['order'] = None
                tickets['position'] = None

        order_position = [False, False]
        time.sleep(0.4)
        
    # Close loose ends and terminate process
    print('Process terminated')
        

def new_process_window():
    new_strategy = widgets()
    return new_strategy


# Placeholder strategy function logic
def function_strategy(data):
    # Simulated logic for BUY/SELL signals based on EMA values
    if data['EMA_20'] > data['EMA_50']:
        return 'BUY'
    elif data['EMA_20'] < data['EMA_50']:
        return 'SELL'
    else:
        return 'HOLD'
