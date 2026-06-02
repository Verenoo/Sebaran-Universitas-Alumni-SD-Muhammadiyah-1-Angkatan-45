from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import csv

# Daftar seluruh siswa Kelas VI (6A - 6F)
daftar_nama = [
    # Kelas 6 A
    "Abdul Waris Syech", "Abidzar Althaffarel", "Akhtar Rakha Hardiansyahputra", "Altaf Nayottama Marhaendra", 
    "Alya Kamila Fauziyah", "Andi Ashilah Dwi Hasni", "Annisa Rifani Putri", "Aura Aziza Hasanah", 
    "Davina Marcelia Putri", "Fadlan Muhammad", "Gendis Khalila Al-fiya", "Hannan Izdihar", 
    "Haura Ramadhani", "Ishaq Athif Ahmadinejad", "Karina Putri Sulistiyowati", "Krisna Teuku Suwito", 
    "Muhammad Adha Rafif Nugroho", "Muhammad Al-mu'tashim Billah Idris", "Muhammad Dhafin Al Khairy", 
    "Muhammad Fasya Andra Ivany Rasya", "Muhammad Hajakbar Adhim", "Muhammad Nirwan Al Fathuri", 
    "Muhammad Rayhan Septiano", "Naila Nabila", "Naiyira Khaalishah Rahman", "Nanda Nabilah Bazighah", 
    "Nayaka Afif Firdhy Qismika", "Nazwa Nabbila Yasmin", "Nur Athifah Pradita Safira", 
    "Nur Ramadhini Putri Nadeak", "Raden Adika Daniswara Jagaddhito", "Ratu Balqis Solehadiranti I.", 
    "Sabrina Prima Cahyana Putri", "Shireen Alfi Zahra Putri", "Vidya Khansa Mizan", "Zhafira Musyaffa Meysun",
    
    # Kelas 6 B
    "Afifah Khairunnisa", "Ahmad Omaar Dzaki Gunawan", "Ahmad Zavier Rifaya Arrazzqa", "Aisyah Az Zahra", 
    "Aisyah Fhariha Mirza", "Akira Muhammad Riano", "Alifah Humaira Putri Amalia", "Alya Afifah Mubarak", 
    "Alya Azzahra", "Andi Raisya Alya Putri Hanafiah", "Anisa Shafiya Amanah", "Azwa Charmaisya Hanny", 
    "Daffa Annafi Ravana", "Dennis Elnata Firstya", "Elvina Alfian", "Galih Mauliddan Rianto", 
    "Ghaitsaa Nadiah Haura", "Hijaz Dwi Nugraha", "Kamila Nadia Ammara", "Kenisha Bunga Kirana", 
    "Mufidah Aulia Rahmah", "Muhammad Farel Al Farisi", "Muhammad Hafi Firdaus", "Muhammad Nirwan Al Farizi", 
    "Muhammad Rafid Putra Vereno", "Muhammad Zayyan Alif", "Nayla Syauqi Aulia", "Nur Hidayah Putri", 
    "Putri Adelia Aathifahsam", "Rafa Eshan Pratama", "Richca Amellia Riedza", "Risa Syahira", 
    "Rizky Al Farizy", "Ronggo Putro Angger Jatmiko", "Yasmin Athir Daniya",
    
    # Kelas 6 C
    "Alfiola Rafia Zhulfa Syahrani", "Aliya Rizky Ramadhani", "Altira Aristid", "Andi Muhammad Alarice Haekal", 
    "Aqyla Vionieza Putri", "Aulia Shifa Alshafiera", "Az-zahra Imsawati Sugianto", "Bahtiar Ardi Muzaki", 
    "Bulan Nayla Ikramina Islami", "Fachria Afiffah Bil Faqih", "Fairus Nadhir Amrullah", "Fharel Fabio Alonso", 
    "Hanna Shelvianofida Mawuntu", "Hasby Naafi Aqiilah", "Kayla Azzahra", "Lydiano Isyabie Putri Pariono", 
    "Maftuh Rizky Arfah Mamonto", "Maulana Ihsaan Sutantyo", "Mohammad Fitriyandi", "Mohammad Kemal Pasha", 
    "Muhammad Chardaffa Pranaja", "Muhammad Daffa Al-isfahani", "Muhammad Diandra Athaya Noviaddin", 
    "Muhammad Fahri Akiela Zhalfa", "Muhammad Rifqi Aunur Rahman", "Muhammad Rijal", "Najwa Syifa Rahimah", 
    "Putri Myli Callula", "Raffi Raidul Halim", "Raisyah Fathir Azzahra", "Refadilah Jundiliansyah", 
    "Reihan Faza Fahrian Rasim", "Rudolf Darren Commas", "Salsabila Putri Malecha", "Siti Humairoh Yasha", 
    "Surya Buana Putra Kamil", "Talitha Kayana Nugroho",

    # Kelas 6 D
    "Ahmad Faiz Akbar", "Ananda Ali Yusuf", "Ananda Ramadana Vidianti", "Andi Nada Bunga Zahra", 
    "Arimbhi Cheyza Prasetya", "Awang Afif Ridhwan Setiawan", "Ayla Faiha Az'zahra", "Az-zahra", 
    "Benning Roufalia Fuwwu Arnotova", "Dendy Rizky Rachmad Ibrohim", "Fachri Bintang Ramadhan", 
    "Farah Tsurrayya", "Firyal Lubna Handayani", "Hafidz Abdurrahman", "Hugo Delfiero", 
    "Lionel Pasha Al Hakim Anwar", "Made Ali Rizqullah Putra Paddengeng", "Michelle Syahkira Herro", 
    "Muhammad Alfaridzi Noor", "Muhammad Aufaa Deyan Putra", "Muhammad Muzhaffir Nailur Raja", 
    "Muhammad Naufal Febrian", "Muhammad Zihad Ra'jab Fadillah", "Nabila Azkiyah", "Nada Qolbu", 
    "Nayaka Baktiadi Hassan", "Nayla Ananda Zahra", "Noval Aulia Ibrahim", "Nur Azizah", "Nurisbaq Alfath", 
    "Rabiatul Awaliyah", "Rafly Islamy Pasha", "Ryan Ardinata Tansir", "Sahlan Dwi Putra", 
    "Salsabilla Choirunissa", "Siti Zulyka", "Syarifah Fathanah Syahab",

    # Kelas 6 E
    "Abdul Ghaniy", "Abel Putra Taryono", "Afif Ahmad Winarno", "Alvira Putri Kirana", 
    "Ananta Hanif Fidzya Pratama", "Andi Muhammad Fazli", "Asri Anggun Meydine Mecca Yusri", "Devina Agustine", 
    "Dliya' Shofaa'", "Dzakiy Rizqi Andika Putra", "Faradiba Muthmaina", "Fatih Arsxha Fajrichzqi Jade", 
    "Fildzah Naylatul Izzah", "Freya Pradipa Aflaha", "Ichwan Raya Enggrayodi", "Imam Ahmad Syantari", 
    "Karina Putri Prasetyawan", "Muhammad Aliifandra", "Muhammad Angga Rizki", "Muhammad Diandra Alhaqki Ramli", 
    "Muhammad Esqi Refanza", "Muhammad Fathir", "Muhammad Fauzan Ramadhan", "Muhammad Husain Hafiz", 
    "Muhammad Ihsan Najmi Nugroho", "Muhammad Marco Pirlo Santoso", "Muhammad Putra Setya Budiono", 
    "Muhammad Rasydan", "Na'illah Arafah Dzahabiyyah", "Nadine Friezilya Putri Widiati", "Nayla Wulan Sari", 
    "Ode Aulianoor", "Raka Adhyra Hard Putra", "Ratih Indria Prabayanti", "Safira Hazrati Zharfa", 
    "Shasha Zasqia", "Whisnu Wijaya Adhen Poetra Budiman",

    # Kelas 6 F
    "Achmad Naufal Rajasa", "Adelya Nafisya", "Adinda Qolbian Mahmudah", "Ahmad Al-fajri Rahman", 
    "Arina Manasikana Nursyaza", "Atila Zaky Nurkhalis", "Audiva Yuriza Cinta Naura", 
    "Awang Muhammad Farras Farfarzsya Putra Mahendra", "Chaerel Ferlan Yamnada", "Chiquita Serendipity Aqila", 
    "Dafva Daniswara", "Dayang Cynthia Pratistha Dewi", "Fathiya Salsabila", "Gusti Anindita Marsa Syaqira", 
    "Kayla Adiva Muttaqin", "Keisha Resendriya", "Keisha Syafrilia", "Kevin Melvino", "Marsya Fina Nur Zahra", 
    "Muhammad Atha Al-fattah", "Muhammad Danish Alghifari", "Muhammad Fachrial Azmi Dian Ramadhan", 
    "Muhammad Farrel Rajwa", "Muhammad Irfan Hafizhurrahman", "Muhammad Rafif Akhdan", "Muhammad Rhino Zacky", 
    "Muhammad Sukri", "Muhammad Zaidan Asy'syakir", "Nada Syafa Rashidah Azhar", "Nadia Ollivia", 
    "Nadia Putri Alya", "Nayla Cahaya Fadillah", "Rasty Aqilah Dhefa", "Sayid Muhammad Ali Alaydrus", 
    "Suci Masawa Arindi", "Syifa Andini"
]

# File CSV diubah namanya agar tidak bercampur
nama_file_csv = "hasil_universitas_lengkap.csv"

with open(nama_file_csv, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Nama Siswa", "Status Pencarian", "Detail Universitas & Jurusan"])

print(f"Total data yang akan diproses: {len(daftar_nama)} siswa.")
print("Membuka Microsoft Edge...")

driver = webdriver.Edge()

for idx, nama in enumerate(daftar_nama, start=1):
    print(f"\n[{idx}/{len(daftar_nama)}] Mencari data: {nama}...")
    status = "Gagal"
    detail_kampus = "-"
    
    try:
        driver.get("https://pddikti.kemdiktisaintek.go.id/search")
        
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Keyword' or @type='text' or contains(@class, 'search')]"))
        )
        
        search_box.clear()
        time.sleep(random.uniform(0.5, 1.5))
        
        for huruf in nama:
            search_box.send_keys(huruf)
            time.sleep(random.uniform(0.05, 0.3)) 
            
        time.sleep(random.uniform(0.5, 1.2)) 
        search_box.send_keys(Keys.RETURN)
        
        waktu_tunggu = random.uniform(5.0, 8.0)
        print(f"   [INFO] Menunggu {waktu_tunggu:.1f} detik untuk hasil loading...")
        time.sleep(waktu_tunggu)
        
        # -------------------------------------------------------------
        # LOGIKA BARU: MEMANJAT KOTAK HASIL UNTUK MENGAMBIL SEMUA TEKS
        # -------------------------------------------------------------
        try:
            # Mencari tombol/link yang menuju profil
            hasil = driver.find_elements(By.XPATH, "//a[contains(@href, '/detail-mhs') or contains(@href, 'mahasiswa') or contains(@href, 'mhs')]")
            
            if len(hasil) > 0:
                elemen_wadah = hasil[0]
                
                # Robot memanjat ke "kotak/wadah" yang lebih besar di atas link tersebut
                for _ in range(5): # Naik maksimal 5 tingkat DOM
                    try:
                        elemen_wadah = elemen_wadah.find_element(By.XPATH, "..")
                        # Jika kotaknya sudah berisi cukup banyak teks (bukan cuma 'Lihat Detail')
                        if len(elemen_wadah.text) > 35: 
                            break
                    except:
                        break
                        
                teks_kotor = elemen_wadah.text
                
                # Membersihkan format teks, mengubah Enter jadi pemisah ( | ), dan membuang tulisan "Lihat Detail"
                teks_bersih = teks_kotor.replace('\n', ' | ').replace(' | Lihat Detail', '').replace('Lihat Detail', '')
                
                status = "Ditemukan"
                detail_kampus = teks_bersih
                print(f"   [BERHASIL] Ditemukan: {detail_kampus}")
            else:
                status = "Data Tidak Ada"
                detail_kampus = "Tidak ada kecocokan nama"
                print("   [KOSONG] Nama tidak ditemukan di database.")
                
        except Exception as read_error:
            status = "Gagal Membaca Web"
            detail_kampus = "Struktur web tidak terbaca"
            print("   [ERROR] Gagal mengekstrak teks hasil.")

    except Exception as e:
        print(f"   [AWAS CAPTCHA / ERROR!] Robot tertahan saat memproses {nama}.")
        print("   >>> 1. Buka jendela Edge yang sedang berjalan.")
        print("   >>> 2. Selesaikan CAPTCHA secara manual (jika ada).")
        print("   >>> 3. Pastikan web sudah kembali ke tampilan normal.")
        
        input("   >>> [TEKAN ENTER DI TERMINAL INI JIKA SUDAH SELESAI] ...")
        
        status = "Bantuan Manual"
        detail_kampus = "Lewati (Terkendala CAPTCHA/Error)"
    
    with open(nama_file_csv, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([nama, status, detail_kampus])
        
    time.sleep(random.uniform(2.0, 4.0))

print(f"\nPROSES SELESAI! Log lengkap tersimpan di file {nama_file_csv}")
driver.quit()