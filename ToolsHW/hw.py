import webbrowser, sys, traceback

VIDEO_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

def input_math():
    try:
        while True:
            user_input = input("1 times 1 = ? ")
            if user_input == 1: 
                webbrowser.open(VIDEO_URL)
                break
            elif user_input == "exit":
                sys.exit()
            else:
                print("Wrong! Try again.")
                webbrowser.open(VIDEO_URL)
    except Exception:
        print("Something went wrong")
        traceback.print_exc()

input_math()
