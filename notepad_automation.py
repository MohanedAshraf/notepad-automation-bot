import os
import time
import requests
import pyautogui
import logging
from pathlib import Path
from botcity.core import DesktopBot

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class NotepadBot(DesktopBot):
    def __init__(self):
        super().__init__()
        self.output_dir = Path.home() / "Desktop" / "tjm-project"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def fetch_posts(self, num_posts=10):
        try:
            response = requests.get("https://jsonplaceholder.typicode.com/posts")
            if response.status_code == 200:
                posts = response.json()
                return posts[:num_posts]
            else:
                logging.error(f"Error fetching posts: {response.status_code}")
                return []
        except Exception as e:
            logging.error(f"Exception while fetching posts: {e}")
            return []
    
    def launch_notepad(self):
        try:
            pyautogui.hotkey('win', 'r')
            time.sleep(0.5)
            pyautogui.write('notepad')
            pyautogui.press('enter')
            time.sleep(1)
            
            if not self.find_notepad_window():
                raise Exception("Failed to find Notepad window")
            
            return True
        except Exception as e:
            logging.error(f"Error launching Notepad: {e}")
            return False
    
    def find_notepad_window(self):
        try:
            window = pyautogui.getWindowsWithTitle('Notepad')
            if window:
                window[0].activate()
                return True
            return False
        except Exception:
            return False
    
    def type_post_content(self, post):
        try:
            content = f"TITLE: {post['title'].upper()}\n\n"
            content += f"Post ID: {post['id']}\n"
            content += f"User ID: {post['userId']}\n\n"
            content += f"{post['body']}\n\n"
            content += "--- End of Post ---"
            
            pyautogui.write(content)
            return True
        except Exception as e:
            logging.error(f"Error typing content: {e}")
            return False
    
    def save_document(self, post_id):
        try:
            pyautogui.hotkey('ctrl', 's')
            time.sleep(1)
            
            file_name = f"post {post_id}.txt"
            file_path = os.path.join(str(self.output_dir), file_name)
            pyautogui.write(file_path)
            time.sleep(0.5)
        
            pyautogui.press('enter')
            time.sleep(1)
            
            try:
                pyautogui.press('left')  
                pyautogui.press('enter')
            except:
                pass
                
            return True
        except Exception as e:
            logging.error(f"Error saving document: {e}")
            return False
    
    def close_notepad(self):
        try:
            pyautogui.hotkey('alt', 'f4')
            time.sleep(0.5)
            
            try:
                pyautogui.press('n')
            except:
                pass
                
            return True
        except Exception as e:
            logging.error(f"Error closing Notepad: {e}")
            return False
    
    def process_posts(self, num_posts=10):
        posts = self.fetch_posts(num_posts)
        if not posts:
            logging.error("No posts to process.")
            return False
        
        successful_posts = 0
        for post in posts:
            try:
                logging.info(f"Processing post {post['id']}...")
                
                if not self.launch_notepad():
                    logging.error(f"Skipping post {post['id']} due to Notepad launch failure.")
                    continue
                
                if not self.type_post_content(post):
                    logging.error(f"Failed to type content for post {post['id']}.")
                    self.close_notepad()
                    continue
                
                if not self.save_document(post['id']):
                    logging.error(f"Failed to save post {post['id']}.")
                    self.close_notepad()
                    continue
                
                self.close_notepad()
                successful_posts += 1
                logging.info(f"Successfully processed post {post['id']}.")
                
                time.sleep(1)
                
            except Exception as e:
                logging.error(f"Error processing post {post['id']}: {e}")
                try:
                    self.close_notepad()
                except:
                    pass
        
        logging.info(f"Successfully processed {successful_posts} out of {len(posts)} posts.")
        return successful_posts == len(posts)

def main():
    logging.info("Starting Notepad Data Entry Bot...")
    bot = NotepadBot()
    
    try:
        logging.info(f"Output directory: {bot.output_dir}")
        success = bot.process_posts(10)
        if success:
            logging.info("All posts successfully processed and saved.")
        else:
            logging.error("Some posts were not processed successfully.")
    except Exception as e:
        logging.error(f"An error occurred during execution: {e}")
    
    logging.info("Notepad Data Entry Bot completed.")

if __name__ == "__main__":
    main()