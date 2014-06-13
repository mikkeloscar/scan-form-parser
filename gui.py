#!/usr/bin/python

from PIL import Image
from gi.repository import Gtk, GdkPixbuf
import io

def img2pixbuf(image):
    """Creates a thumbnail GdkPixbuf of given image (PIL)"""
    # Convert to GdkPixbuf
    if image.mode != 'RGB':          # Fix IOError: cannot write mode P as PPM
        image = image.convert('RGB')
    buff = io.BytesIO()
    image.save(buff, 'ppm')
    contents = buff.getvalue()
    buff.close()
    loader = GdkPixbuf.PixbufLoader.new_with_type('pnm')
    loader.write(contents)
    pixbuf = loader.get_pixbuf()
    loader.close()

    return pixbuf


class GTKImage(Gtk.Image):

    def __init__(self, image, size=(100,100)):
        Gtk.Image.__init__(self)
        image = image.resize(size)
        pixbuf = img2pixbuf(image)
        self.set_from_pixbuf(pixbuf)


class Application(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Scan form parser")

        self.set_default_size(400, 300)
        self.set_border_width(20)

        # initialize file UI
        self.file_ui()

        # add it to Gtk.Window
        self.add(self.file_ui)


    def file_ui(self):
        self.file_ui = Gtk.Table(3, 3, True)

        file_btn = Gtk.Button("Vælg scanner fil")
        file_btn.connect("clicked", self.on_file_clicked)
        self.file_ui.attach(file_btn, 1, 2, 1, 2)


    def cpr_ui(self, cpr_image="", id_image=""):

        self.cpr_ui = Gtk.Table(3, 1, True)

        id_image = Image.open("1203901956.jpg")
        cpr_image = Image.open("tmp-id.png")

        image_cpr = GTKImage(cpr_image, (290,80))
        image_id = GTKImage(id_image)
        cpr_txt = Gtk.Label("CPR")
        self.cpr_entry = Gtk.Entry()
        accept_btn = Gtk.Button("Gem")
        accept_btn.connect("clicked", self.on_button_clicked)

        input_box = Gtk.Box(spacing=6)
        input_box.pack_start(cpr_txt, True, True, 0)
        input_box.pack_start(self.cpr_entry, True, True, 0)
        input_box.pack_start(accept_btn, True, True, 0)
        self.cpr_ui.attach(image_cpr, 0, 1, 0, 1)
        self.cpr_ui.attach(input_box, 0, 1, 1, 2)
        self.cpr_ui.attach(image_id, 0, 1, 2, 3)


    def on_file_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a file", self,
                Gtk.FileChooserAction.OPEN,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                    Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def add_filters(self, dialog):
        filter_pdf = Gtk.FileFilter()
        filter_pdf.set_name("PDF files")
        filter_pdf.add_mime_type("application/pdf")
        dialog.add_filter(filter_pdf)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def on_button_clicked(self, widget):
        print("Hello World")

    def on_btn_next_clicked(self, widget):
        cpr = self.cpr_entry.get_text()
        print(cpr)
        self.remove(self.file_ui)
        self.cpr_ui()
        self.add(self.cpr_ui)
        self.show_all()

if __name__ == "__main__":
    win = Application()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
