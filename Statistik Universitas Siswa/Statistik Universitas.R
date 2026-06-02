library(ggplot2)
library(dplyr)
library(stringr)
library(readr)

file_input <- "C:/Users/ASUS/Downloads/Data Universitas SD Muhammadiyah 1 Angkatan 45/hasil_universitas_lengkap.csv"
folder_output <- "Grafik_Kampus"

if (!dir.exists(folder_output)) {
  dir.create(folder_output)
  cat(sprintf("Folder '%s' berhasil dibuat.\n", folder_output))
}

daftar_kampus <- c(
  "UNIVERSITAS INDONESIA", "UNIVERSITAS GADJAH MADA", "INSTITUT TEKNOLOGI BANDUNG", 
  "INSTITUT TEKNOLOGI SEPULUH NOPEMBER", "UNIVERSITAS AIRLANGGA", "UNIVERSITAS DIPONEGORO", 
  "UNIVERSITAS BRAWIJAYA", "UNIVERSITAS MULAWARMAN", "UNIVERSITAS MUHAMMADIYAH KALIMANTAN TIMUR", 
  "UNIVERSITAS TERBUKA", "INSTITUT TEKNOLOGI KALIMANTAN", "UNIVERSITAS NEGERI SEMARANG", 
  "UNIVERSITAS NEGERI MALANG", "UNIVERSITAS NEGERI SURABAYA", "POLITEKNIK NEGERI SAMARINDA", 
  "UNIVERSITAS ANDALAS", "UNIVERSITAS ISLAM INDONESIA", "UNIVERSITAS BINA NUSANTARA", 
  "UNIVERSITAS 17 AGUSTUS 1945 SAMARINDA", "UNIVERSITAS ISLAM NEGERI MAULANA MALIK IBRAHIM", 
  "UNIVERSITAS ISLAM NEGERI SUNAN AMPEL", "UNIVERSITAS ISLAM NEGERI SUNAN KALIJAGA", 
  "STMIK WIDYA CIPTA DHARMA", "UNIVERSITAS GUNADARMA", "UNIVERSITAS TULANG BAWANG", 
  "SEKOLAH TINGGI TEKNOLOGI MIGAS", "UNIVERSITAS PEMBANGUNAN NASIONAL VETERAN YOGYAKARTA", 
  "UNIVERSITAS ISLAM LAMONGAN", "INSTITUT TEKNOLOGI KESEHATAN DAN SAINS WIYATA HUSADA SAMARINDA", 
  "UNIVERSITAS TRISAKTI", "STIKES MOHAMMAD HUSNI THAMRIN", "INSTITUT DIGITAL EKONOMI LPKIA", 
  "UNIVERSITAS KRISNADWIPAYANA", "INSTITUT SENI INDONESIA YOGYAKARTA", "UNIVERSITAS PRESIDEN", 
  "UNIVERSITAS TELKOM", "UNIVERSITAS DAYANU IKHSANUDDIN", "UNIVERSITAS SUMATERA UTARA", 
  "UNIVERSITAS PASUNDAN", "POLITEKNIK NEGERI UJUNG PANDANG", "UNIVERSITAS TRIBHUWANA TUNGGA DEWI", 
  "POLTEKKES KEMENKES SURAKARTA", "UNIVERSITAS MERCU BUANA", "UNIVERSITAS BOROBUDUR", 
  "UNIVERSITAS PANCASILA", "UNIVERSITAS AMIKOM YOGYAKARTA", "UNIVERSITAS KUNINGAN", "UNIVERSITAS SAMAWA"
)

cat("Membaca dan memisahkan data Jurusan...\n")

# 1. Membaca dan Membersihkan Data
data_mentah <- read_csv(file_input, show_col_types = FALSE)

data_bersih <- data_mentah %>%
  filter(`Status Pencarian` == "Ditemukan", 
         !str_detect(`Detail Universitas & Jurusan`, "Silakan cari kata kunci lain")) %>%
  rowwise() %>%
  mutate(
    NIM = str_extract(`Detail Universitas & Jurusan`, "\\b\\d{6,}\\b"),
    Sisa_Teks = ifelse(!is.na(NIM), str_trim(str_split(`Detail Universitas & Jurusan`, NIM, n = 2)[[1]][2]), `Detail Universitas & Jurusan`),
    Universitas = "KAMPUS LAINNYA",
    Jurusan = Sisa_Teks
  ) %>%
  ungroup()

for (i in 1:nrow(data_bersih)) {
  teks <- data_bersih$Jurusan[i]
  for (kampus in daftar_kampus) {
    if (str_detect(teks, fixed(kampus))) {
      data_bersih$Universitas[i] <- kampus
      data_bersih$Jurusan[i] <- str_trim(str_replace(teks, fixed(kampus), ""))
      break
    }
  }
  if (data_bersih$Jurusan[i] == "" || is.na(data_bersih$Jurusan[i])) {
    data_bersih$Jurusan[i] <- "TIDAK DIKETAHUI"
  }
}

cat("Membuat grafik per universitas (menyimpan ke folder)...\n")

kampus_unik <- unique(data_bersih$Universitas)

for (kampus in kampus_unik) {
  df_kampus <- data_bersih %>% 
    filter(Universitas == kampus) %>%
    count(Jurusan, name = "Jumlah")
  
  plot_kampus <- ggplot(df_kampus, aes(x = reorder(Jurusan, -Jumlah), y = Jumlah)) +
    geom_col(fill = "skyblue", color = "black") +
    labs(title = paste("Sebaran Jurusan di", kampus),
         x = "Jurusan",
         y = "Jumlah Siswa") +
    theme_minimal() +
    theme(
      plot.title = element_text(face = "bold", size = 14, hjust = 0.5),
      axis.text.x = element_text(angle = 45, hjust = 1) # Memiringkan teks jurusan
    )

  nama_file <- paste0(folder_output, "/", str_replace_all(kampus, " ", "_"), ".png")
  ggsave(nama_file, plot = plot_kampus, width = 8, height = 6, dpi = 150, bg = "white")
}

cat("Membuat grafik keseluruhan jurusan...\n")

df_total <- data_bersih %>% count(Jurusan, name = "Jumlah")
tinggi_gambar <- max(8, nrow(df_total) * 0.3)

plot_total <- ggplot(df_total, aes(x = Jumlah, y = reorder(Jurusan, Jumlah))) +
  geom_col(fill = "coral", color = "black") +
  labs(title = "Grafik Keseluruhan Peminatan Jurusan Siswa",
       x = "Total Siswa",
       y = "Jurusan") +
  theme_minimal() +
  theme(
    plot.title = element_text(face = "bold", size = 16, hjust = 0.5)
  )

ggsave("Grafik_Total_Semua_Jurusan.png", plot = plot_total, width = 12, height = tinggi_gambar, dpi = 200, limitsize = FALSE, bg = "white")

cat("Selesai! Silakan cek folder document\n")

