import os
import requests
import logging
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import threading
 
 
# Suppress INFO logs from the image_downloader logger
logging.getLogger("image_downloader").setLevel(logging.WARNING)
 
 
# Suppress debug logs from urllib3 and chardet
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("chardet").setLevel(logging.WARNING)
 
 
# Setup logging for monitoring operations
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('image_downloader')
 
 
# Setup logging for monitoring operations
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('image_downloader')
 
 
 
 
def check_url_validity(web_url):
   """
   Verifies if the provided URL is well-formed and valid.
   """
   parsed_url = urlparse(web_url)
   return parsed_url.netloc and parsed_url.scheme
 
 
 
 
def extract_image_urls(web_page_url):
   """
   Collects and returns all the image URLs found on the provided web page URL.
   """
   try:
       page_response = requests.get(web_page_url, headers={'User-Agent': 'Custom User Agent'})
       page_response.raise_for_status()
       html_parser = BeautifulSoup(page_response.content, "html.parser")
       image_urls = []
       for image_tag in html_parser.find_all("img"):
           image_source = image_tag.get("src")
           if image_source:
               full_image_url = urljoin(web_page_url, image_source)
               full_image_url = full_image_url.split("?")[0]  # Strip URL parameters
               if check_url_validity(full_image_url):
                   image_urls.append(full_image_url)
       return image_urls
   except Exception as error:
       log.error(f"Failed to fetch images from {web_page_url}: {error}")
       return []
 
 
 
 
def save_image(image_url, target_folder):
   """
   Downloads and saves an image from its URL to the specified directory.
   """
   if not os.path.exists(target_folder):
       os.makedirs(target_folder)
 
 
   try:
       with requests.get(image_url, stream=True) as response:
           response.raise_for_status()
           file_path = os.path.join(target_folder, os.path.basename(image_url))
 
 
           with open(file_path, "wb") as file:
               for chunk in response.iter_content(chunk_size=1024):
                   file.write(chunk)
 
 
           log.info(f"Image saved: {file_path}")
   except Exception as error:
       log.error(f"Failed to download {image_url}: {error}")
 
 
 
 
def fetch_and_save_images(main_url, save_path):
   """
   Main function to retrieve and store images from a given URL.
   """
   images = extract_image_urls(main_url)
   for image in images:
       save_image(image, save_path)
   messagebox.showinfo("Download Complete", "All images have been downloaded.")
 
 
 
 
def start_download_process():
   entered_url = url_input.get()
   save_directory = directory_input.get()
   if not check_url_validity(entered_url):
       messagebox.showerror("Error", "The URL entered is not valid.")
       return
 
 
   # Start the download process in a separate thread
   download_thread = threading.Thread(target=fetch_and_save_images, args=(entered_url, save_directory))
   download_thread.start()
 
 
   messagebox.showinfo("Download Started", "Image download process has started.")
 
 
 
 
def choose_directory():
   folder_selected = filedialog.askdirectory()
   if folder_selected:
       directory_input.delete(0, tk.END)
       directory_input.insert(0, folder_selected)
 
 
 
 
# GUI Setup
root = tk.Tk()
root.title("Image Downloader - The Pycodes")
 
 
url_label = ttk.Label(root, text="Enter URL:")
url_label.grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)
url_input = ttk.Entry(root, width=50)
url_input.grid(column=1, row=0, padx=5, pady=5, sticky=tk.EW)
 
 
directory_label = ttk.Label(root, text="Save Images To:")
directory_label.grid(column=0, row=1, padx=5, pady=5, sticky=tk.W)
directory_input = ttk.Entry(root, width=50)
directory_input.grid(column=1, row=1, padx=5, pady=5, sticky=tk.EW)
browse_button = ttk.Button(root, text="Browse", command=choose_directory)
browse_button.grid(column=2, row=1, padx=5, pady=5)
 
 
download_btn = ttk.Button(root, text="Start Download", command=start_download_process)
download_btn.grid(column=0, row=2, columnspan=3, padx=5, pady=5, sticky=tk.EW)
 
 
root.mainloop()
