import tkinter as tk
import requests

class Dup_Popup(object):
    root=None
    def __init__(self,query=[],orig=[],dict_key=None):
        self.top = tk.Toplevel(Dup_Popup.root)
        self.top.grab_set()

        self.msg=tk.Label(self.top,text="Record(s) with the same MAC Address as this record already exist(s) in inventory.\nRecord in pending devices:\n"+", ".join(query)+"\nRecord(s) with same MAC address in inventory:\n"+", ".join(orig))
        self.msg.pack(side='top')

        self.btn_frame=tk.Frame(self.top)
        self.btn_frame.pack(side='top')

        self.opt1=tk.Button(self.btn_frame,text='skip duplicate',command=lambda:self.opt1_func(query, dict_key))
        self.opt1.pack(side='left',padx=4)
        self.opt2=tk.Button(self.btn_frame,text='replace existing',command=lambda:self.opt2_func(orig,query, dict_key))
        self.opt2.pack(side='left',padx=4)
        self.opt3=tk.Button(self.btn_frame,text='keep both',command=lambda:self.opt3_func(query, dict_key))
        self.opt3.pack(side='left',padx=4)

        Dup_Popup.root.wait_window(self.top)

    def opt1_func(self,query,dict_key):
        x=requests.get("http://172.30.211.33:5000/run_sql?command=DELETE FROM pending_devices WHERE Id="+query[0][1:-1]+"&cmdtype=write&auth=token")
        dict_key['opt'] = '1'
        self.top.destroy()
        
    def opt2_func(self,orig,query,dict_key):
        x=requests.get("http://172.30.211.33:5000/run_sql?command=DELETE FROM pending_devices WHERE Id="+query[0][1:-1]+"&cmdtype=write&auth=token")
        x=requests.get("http://172.30.211.33:5000/run_sql?command=UPDATE devices SET Brand = "+query[1]+", Model = "+query[2]+", Serial_Number = "+query[3]+", MAC_Address = "+query[4]+", Universal_Product_Code = "+query[5]+", Uploader_Name = "+query[6]+", Scan_Date = datetime("+query[7]+"), Recipient = "+query[8]+", Paid_Amount = "+query[9]+", Vendor = "+query[10]+", Invoice_IPO = "+query[11]+", PO_Registered = "+query[12]+", InControl_Expiration = "+query[13]+", Notes = "+query[14]+" WHERE Id="+str(orig[0])+"&cmdtype=write&auth=token")
        dict_key['opt']='2'
        print(dict_key)
        self.top.destroy()

    def opt3_func(self,query,dict_key):
        dict_key['opt']='3'
        self.top.destroy()
        
