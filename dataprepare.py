import os
import shutil

def delete_non_html_txt_files(root_folder, destination_folder):
 
    global count
    files = os.listdir(root_folder)
    
    for file_name in files:
        file_path = os.path.join(root_folder, file_name)
        
        if os.path.isdir(file_path):
         
            delete_non_html_txt_files(file_path, destination_folder)
        else:
            if file_name == "html.txt":
                destination_path = os.path.join(destination_folder, str(count) + ".txt")
                shutil.move(file_path, destination_path)
                print(f"{file_path} successfully moved to the {destination_folder} folder and renamed as ", str(count) + ".txt")
                count += 1
             
            


def extract_data(root_folder):
        global count
        legitimate_path = os.path.join(root_folder, "Legitimate")
        try:
            os.makedirs(legitimate_path)
        except FileExistsError:
            pass
        phising_path = os.path.join(root_folder, "Phishing")
        try:
            os.makedirs(phising_path)
        except FileExistsError:
            pass
        
        legitimate = os.path.join(root_folder, "benign_25k")
        phishing = os.path.join(root_folder, "phish_sample_30k")
        misleading = os.path.join(root_folder, "misleading")

        delete_non_html_txt_files(legitimate, legitimate_path)
        #count = 0
        print("Deleting ", legitimate, " and it's ingredients...")
        shutil.rmtree(legitimate)
        
        delete_non_html_txt_files(misleading, legitimate_path)
        print("Deleting ", misleading, " and it's ingredients...")
        shutil.rmtree(misleading)
        
        count = 0

        delete_non_html_txt_files(phishing, phising_path)
        print("Deleting ", phishing, " and it's ingredients...")
        shutil.rmtree(phishing)

        print("Finished.\nAll unnecessary files and folders in the " + root_folder + " have been cleaned succesfully and the importants grouped in \\Legitimate and \\Phishing folders.")

        

#main
root_folder = "PhishIntention"#change with relative path
count = 0 #moved file new name, must be 0
extract_data(root_folder)



