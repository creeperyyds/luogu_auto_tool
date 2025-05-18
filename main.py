import webview, tkinter
loadok = False
f = open('aa', 'w+', encoding='utf-8')
def readpage_records(window: webview.Window) -> None:
    global loadok
    for e in window.dom.get_elements('div.row-wrap')[0].children:
        for p in e.text.splitlines()[3:]:
            f.write(p.strip())
            f.write(' ')
        f.write('\n')
    f.flush()
    print('f')
    loadok = True
def after_loaded_records(window: webview.Window) -> None:
    global loadok
    cookie_with_uid = window.get_cookies()[1].output()[17:]
    if int(cookie_with_uid[:cookie_with_uid.find(';')]) == 0:
        window.create_confirmation_dialog('提示', '请在洛谷中完成登录')
        return
    if window.get_current_url() != 'https://www.luogu.com.cn/record/list?user=0':
        window.load_url('https://www.luogu.com.cn/record/list?user=0')
        return
    window.events.loaded -= after_loaded_records
    window.events.loaded += readpage_records
    readpage_records(window)
    for now_page in range(2, int(window.dom.get_elements('span.total')[0].children[0].text) + 1):
        while not loadok: pass
        loadok = False
        window.load_url(f'https://www.luogu.com.cn/record/list?user=0&page={now_page}')
    while not loadok: pass
    window.destroy()
def after_loaded_auto_punch(window: webview.Window) -> None:
    ele = window.dom.get_element('a[name]')
    if not ele is None and ele.attributes['name'] == 'punch': print(window.evaluate_js('document.querySelector("a[name]").click()'))
'''webview.create_window('也许算个爬虫？', 'https://www.luogu.com.cn/record/list?user=0', hidden=True).events.loaded += after_loaded
webview.start(private_mode=False)'''
# document.getElementsByClassName('input-group')[0].children[0].value = 23030
webview.create_window('aaa', 'https://www.luogu.com.cn').events.loaded += after_loaded_auto_punch
webview.start(private_mode=False)