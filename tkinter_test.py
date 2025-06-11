import tkinter as tk
import os

# macOS에서 Tkinter 관련 경고를 숨기기 위함 (선택 사항)
os.environ['TK_SILENCE_DEPRECATION'] = '1'

def main():
    print("DEBUG: tkinter_test.py - main() started")
    try:
        root = tk.Tk()
        root.title("Tkinter Test")
        root.geometry("300x200")
        print("DEBUG: tk.Tk() instance created")

        # Try with a background color and no specific font
        label = tk.Label(root, text="Hello, Tkinter!", padx=20, pady=20, bg='lightgreen') 
        label.pack(expand=True)
        print("DEBUG: tk.Label created and packed with background")

        # Force update of the window
        print("DEBUG: Calling root.update_idletasks()")
        root.update_idletasks()
        print("DEBUG: Calling root.update()")
        root.update() # Try forcing a redraw

        # 창이 바로 닫히지 않도록 버튼 추가 (선택 사항)
        # def close_window():
        #     print("DEBUG: Closing window")
        #     root.destroy()
        # close_button = tk.Button(root, text="Close", command=close_window)
        # close_button.pack(pady=10)

        print("DEBUG: Calling root.mainloop()")
        root.mainloop()
        print("DEBUG: root.mainloop() finished") # This will print when the window is closed

    except Exception as e:
        print(f"ERROR in tkinter_test.py: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
