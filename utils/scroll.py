import sys
import tkinter as tk

# Reusable scrollable Tkinter Frame
class ScrollableFrame(tk.Frame):
    """
    A special Frame to pack widgets into that scrolls like a normal panel.

    Usage:
        frame = ScrollableFrame(root)
        frame.pack(**whatever_args)
        # pack direct children under frame.scrollable_frame
        child = tk.Label(frame.scrollable_frame, text="hello").pack()
    """

    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.MIN_WIDTH = 700
        self.MIN_HEIGHT = 700

        bg = kwargs.get("bg")

        self.canvas = tk.Canvas(self, highlightthickness=0, bg=bg)

        self.y_scrollbar_cont = tk.Frame(self, bg=bg, padx=0, pady=0)
        self.y_scrollbar = tk.Scrollbar(self.y_scrollbar_cont, orient="vertical", command=self.canvas.yview)
        self.y_scrollbar_cont.pack(side="right", fill="y")

        self.x_scrollbar_cont = tk.Frame(self, bg=bg, padx=0, pady=0)
        self.x_scrollbar = tk.Scrollbar(self.x_scrollbar_cont, orient="horizontal", command=self.canvas.xview)
        self.x_scrollbar_cont.pack(side="bottom", fill="x")

        # Put real content inside this frame, not ScrollableFrame itself
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg)

        self.scrollable_frame.bind(
            "<Configure>",
            self._on_frame_configure,
        )

        self.window_id = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )
        self.canvas.configure(yscrollcommand=self.y_scrollbar.set, xscrollcommand=self.x_scrollbar.set)

        self.canvas.bind(
            "<Configure>",
            lambda e: self._on_canvas_configure(e),
        )

        self.canvas.pack(side="left", fill="both", expand=True)

    def _on_mousewheel(self, event, scroll_type):

        # Windows and macOS
        if event.delta:
            if sys.platform == "darwin":
                # macOS often provides smaller, trackpad-style delta values
                amount = -event.delta
            else:
                # Windows commonly changes in increments of 120
                amount = -(event.delta // 120)
        else:
            return

        if scroll_type == "x":
            self.canvas.xview_scroll(amount, "units")
        else:
            self.canvas.yview_scroll(amount, "units")
        
    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        canvas_height = event.height
        canvas_width = event.width

        if canvas_width < self.MIN_WIDTH:
            self.x_scrollbar.pack(fill="x", expand=True)
            self.canvas.bind_all("<Shift-MouseWheel>", lambda e: self._on_mousewheel(e, scroll_type="x"))

            self.canvas.itemconfig(self.window_id, width=self.MIN_WIDTH)
        else:
            try:
                self.x_scrollbar.pack_forget()
            except Exception as e:
                pass

            try:
                self.canvas.unbind("<Shift-MouseWheel>", "")
            except Exception as e:
                pass

            self.canvas.itemconfig(self.window_id, width=canvas_width)

        if canvas_height < self.MIN_HEIGHT:
            self.y_scrollbar.pack(fill="y", expand=True)
            self.canvas.bind_all("<MouseWheel>", lambda e: self._on_mousewheel(e, scroll_type="y"))
            
            self.canvas.itemconfig(self.window_id, height=self.MIN_HEIGHT)
        else:
            try:
                self.y_scrollbar.pack_forget()
            except Exception as e:
                pass

            try:
                self.canvas.unbind("<MouseWheel>", "")
            except Exception as e:
                pass
            
            self.canvas.itemconfig(self.window_id, height=canvas_height)