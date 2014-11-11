import web
from web import form
from backend import make_triplicates

render = web.template.render('templates/')

urls = (
        '/upload', 'Upload',
        '/index', 'index'
    )

class Upload:
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return render.upload()

    def POST(self):
        x = web.input(myfile={})
        filedir = 'csv_files/'
        if 'myfile' in x: # to check if the file-object is created
            fout = open(filedir + '/rawdata.csv', 'w') # creates the file where the uploaded file should be stored
            lines = x.myfile.file.readlines()
            for line in lines:
                nline = line.replace(',', '.')
                fout.write(nline)
            fout.close() # closes the file, upload complete.
        raise web.seeother('/index')

class index:
    def GET(self):
        return render.index()

    def POST(self):
        form = web.input(a='', b='', c='', d='', e='', f='', g='', h='',\
                         one='', two='', three='', four='', five='', six='',\
                         seven='', eight='', nine='', ten='', eleven='', twelve='',\
                         plot_this = '', errorbars = '', measurement = '')
        a, b, c, d, e, f, g, h = (form.a, form.b, form.c, form.d, form.e, form.f, form.g, form.h)
        one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve = (form.one, form.two, form.three,\
            form.four, form.five, form.six, form.seven, form.eight, form.nine, form.ten, form.eleven, form.twelve)
        plot_this = form.plot_this
        strains = {'A': a, 'B': b, 'C': c, 'D': d, 'E': e, 'F': f, 'G': g, 'H': h}
        conditions = {'1': one, '2': two, '3': three, '4': four, '5': five, '6': six,\
                      '7': seven, '8': eight, '9': nine, '10': ten, '11': eleven,\
                      '12': twelve}
        plot_this = plot_this.split(';')
        plot_this = [x.replace(' ', '').split(',') for x in plot_this]
        errorbars = form.errorbars

        make_triplicates('csv_files/rawdata.csv', plot_this, conditions, strains, errorbars = errorbars)
        raise web.seeother('/static/showme.png')


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
