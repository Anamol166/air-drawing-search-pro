import cv2
import numpy as np
import webbrowser
from hand import HandTracker
from model import RecognitionEngine

class AirDrawingApp:
    def __init__(self):
        #window dimensions
        self.W, self.H = 1280, 720
        self.tracker = HandTracker()
        
        #ai models for recognition
        self.engine = RecognitionEngine("bModel.h5", "bestmodel.h5", "drawing.h5", "class.txt")
        
        #drawing canvas 
        self.canvas = np.zeros((self.H, self.W, 3), np.uint8)
        self.mode = "ALPHA"  
        self.color_idx = 0
        self.shape_idx = 0
        self.shape_list = ["Line", "Rectangle", "Circle"]
        self.colors = [(0,0,255), (0,255,0), (255,0,0), (0,255,255), (255,0,255), (1,1,1), (0,0,0)]
        self.color_names = ["RED", "GREEN", "BLUE", "YELLOW", "PINK", "BLACK", "ERASER"]
        self.smooth_x, self.smooth_y = 0, 0
        self.prev_x, self.prev_y = 0, 0
        self.shape_start = None
        self.recognized_raw = ""
        self.corrected_txt = ""
        self.is_fullscreen = False

    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, self.W)
        cap.set(4, self.H)
        win_name = "Air Drawing Search Pro"
        cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
        
        while True:
            success, img = cap.read()
            if not success: break
            img = cv2.flip(img, 1) 
            
            img = self.tracker.find_hands(img)
            lm_list = self.tracker.get_landmark_list(img)
            
           #ui
            overlay = img.copy()
            cv2.rectangle(overlay, (0,0), (self.W, 100), (20, 20, 20), -1)
            cv2.addWeighted(overlay, 0.7, img, 0.3, 0, img)
            
            bw = self.W // len(self.colors)
            for i, col in enumerate(self.colors):
                #drawcolor
                box_color = (50, 50, 50) if i == 5 else col 
                cv2.rectangle(img, (i*bw+15, 15), ((i+1)*bw-15, 65), box_color, -1)
                
                if i == self.color_idx: 
                    cv2.rectangle(img, (i*bw+12, 12), ((i+1)*bw-12, 68), (255,255,255), 2)
                
                cv2.putText(img, self.color_names[i], (i*bw+bw//4, 85), 0, 0.4, (200, 200, 200), 1)

           #hand tracking and drawing logic
            if lm_list:
                fingers = self.tracker.get_fingers_up(lm_list)
                cx, cy = lm_list[8][1], lm_list[8][2]   # Index Tip
                mx, my = lm_list[12][1], lm_list[12][2] # Middle Tip
                self.smooth_x = int(0.65 * cx + 0.35 * self.smooth_x)
                self.smooth_y = int(0.65 * cy + 0.35 * self.smooth_y)

                #selection mode
                if fingers[1] and fingers[2] and fingers[3]:
                    self.prev_x, self.prev_y = 0, 0
                    self.shape_start = None 
                    cv2.circle(img, (mx, my), 10, (255, 255, 255), cv2.FILLED) 
                    cv2.circle(img, (mx, my), 14, (200, 200, 200), 2)           
                    
                    if my < 100: 
                        self.color_idx = mx // bw
                        self.color_idx = min(self.color_idx, len(self.colors)-1)
                
                #shape preview
                elif fingers[1] and fingers[2]:
                    self.prev_x, self.prev_y = 0, 0 
                    if not self.shape_start: 
                        self.shape_start = (self.smooth_x, self.smooth_y)
                    self.draw_preview(img)
                
                #index
                elif fingers[1]:
            
                    if self.shape_start:
                        dist = np.hypot(self.smooth_x - self.shape_start[0], self.smooth_y - self.shape_start[1])
                        if dist > 20:
                            self.draw_to_canvas(self.canvas)
                        self.shape_start = None
                    
                    if self.prev_x == 0: 
                        self.prev_x, self.prev_y = self.smooth_x, self.smooth_y
                    
                    thick = 100 if self.color_idx == 6 else 5
                    cv2.line(self.canvas, (self.prev_x, self.prev_y), (self.smooth_x, self.smooth_y), 
                             self.colors[self.color_idx], thick)
                    self.prev_x, self.prev_y = self.smooth_x, self.smooth_y
                
                else:
                    self.prev_x, self.prev_y = 0, 0
                    self.shape_start = None

            img_gray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY)
            img = cv2.add(cv2.bitwise_and(img, img, mask=cv2.bitwise_not(mask)), self.canvas)
        
            fy = self.H - 85
    
            footer_overlay = img.copy()
            cv2.rectangle(footer_overlay, (0, fy), (self.W, self.H), (20, 20, 20), -1)
            cv2.addWeighted(footer_overlay, 0.85, img, 0.15, 0, img)
            cv2.line(img, (0, fy), (self.W, fy), (0, 255, 255), 2) 
            
            # Left Section: Status
            cv2.putText(img, "MODE:", (20, self.H-50), 0, 0.5, (150, 150, 150), 1)
            cv2.putText(img, f"{self.mode}", (20, self.H-20), 0, 0.7, (0, 255, 255), 2)
            
            cv2.putText(img, "TOOL:", (160, self.H-50), 0, 0.5, (150, 150, 150), 1)
            cv2.putText(img, self.shape_list[self.shape_idx].upper(), (160, self.H-20), 0, 0.6, (200, 200, 200), 1)
         #result display
            res_display = self.recognized_raw if self.recognized_raw else "---"
            if self.corrected_txt and self.corrected_txt != self.recognized_raw:
                res_display = f"{self.recognized_raw} -> {self.corrected_txt}"
            
            cv2.putText(img, "RECOGNITION RESULT:", (350, self.H-50), 0, 0.5, (150, 150, 150), 1)
            cv2.putText(img, res_display, (350, self.H-20), 0, 0.8, (0, 255, 0), 2)

            #keyboard shortcuts
            shortcut_x = 820
            cv2.putText(img, "[R] RECO  |  [F] FULL  |  [S] SHAPE", (shortcut_x, self.H-50), 0, 0.5, (180, 180, 180), 1)
            cv2.putText(img, "[C] CLEAR |  [A/N/D] MODES |  [ENTER] SEARCH", (shortcut_x, self.H-20), 0, 0.5, (180, 180, 180), 1)

            cv2.imshow(win_name, img)

            #shortcuts
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'): break
            if key == ord('c'):
                self.canvas[:] = 0
                self.recognized_raw, self.corrected_txt = "", ""
            if key == ord('a'): self.mode = "ALPHA"
            if key == ord('n'): self.mode = "NUM"
            if key == ord('d'): self.mode = "DRAW"
            if key == ord('s'): self.shape_idx = (self.shape_idx + 1) % 3
            if key == ord('f'): 
                self.is_fullscreen = not self.is_fullscreen
                cv2.setWindowProperty(win_name, cv2.WND_PROP_FULLSCREEN, 
                                      cv2.WINDOW_FULLSCREEN if self.is_fullscreen else cv2.WINDOW_NORMAL)
            if key == ord('r'): self.handle_recognition()
            if key == 13: # Enter key search
                final_q = self.corrected_txt if self.corrected_txt else self.recognized_raw
                if final_q: webbrowser.open(f"https://www.google.com/search?q={final_q}")

        cap.release()
        cv2.destroyAllWindows()

    def draw_preview(self, img):
        col = self.colors[self.color_idx] if self.color_idx < 6 else (255,255,255)
        s = self.shape_list[self.shape_idx]
        if s == "Rectangle": cv2.rectangle(img, self.shape_start, (self.smooth_x, self.smooth_y), col, 2)
        elif s == "Circle":
            r = int(np.hypot(self.smooth_x - self.shape_start[0], self.smooth_y - self.shape_start[1]))
            cv2.circle(img, self.shape_start, r, col, 2)
        elif s == "Line": cv2.line(img, self.shape_start, (self.smooth_x, self.smooth_y), col, 2)

    def draw_to_canvas(self, target):
        col = self.colors[self.color_idx]
        s = self.shape_list[self.shape_idx]
        if s == "Rectangle": cv2.rectangle(target, self.shape_start, (self.smooth_x, self.smooth_y), col, 5)
        elif s == "Circle":
            r = int(np.hypot(self.smooth_x - self.shape_start[0], self.smooth_y - self.shape_start[1]))
            cv2.circle(target, self.shape_start, r, col, 5)
        elif s == "Line": cv2.line(target, self.shape_start, (self.smooth_x, self.smooth_y), col, 5)

    def handle_recognition(self):
        gray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        if self.color_idx == 5: 
             _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
        else:
             _, th = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
        
        if self.mode == "DRAW":
            self.recognized_raw = self.engine.predict_drawing(th)
            self.corrected_txt = ""
        else:
            raw, corrected = self.engine.predict_text(th, self.mode)
            self.recognized_raw, self.corrected_txt = raw, corrected

if __name__ == "__main__":
    app = AirDrawingApp()
    app.run()
