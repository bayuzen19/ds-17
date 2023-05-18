import streamlit as st

def main():
    #---- mengatur lebar tampilan -----
    st.markdown('<style>body{max-width: 800px; margin: auto;}</style>', unsafe_allow_html=True)
    


# Judul halaman
    st.title("📝 Resume")

    # Menambahkan foto profil
    profile_pic = "images/foto_cv.jpeg"
    st.image(profile_pic, caption='Foto Profil', use_column_width=False, output_format='JPEG', width=150,)

    # Informasi pribadi
    st.header("About Me 😊")
    st.write("As a versatile data professional, I specialize in data science, data analysis, data engineering, front-end development, and computer vision. With expertise in Python, R, JavaScript, React, HTML, CSS, Power BI, Tableau, Excel, Spark, SQL, machine learning, and deep learning, I am well-equipped to deliver powerful insights and solutions across various domains.")
    st.write("I hold a degree in Materials and Metallurgical Engineering from the Sepuluh Nopember Institute of Technology and currently serve as a Data Scientist. Over the past years, I have completed numerous training programs focused on honing my data science skills and have contributed to several data-related projects.")
    st.write("My experience in Impala, Spark, and other cutting-edge technologies enables me to deliver high-quality solutions that drive business success. I am passionate about using data to inform decision-making and solve complex business challenges. I thrive in fast-paced, collaborative environments and am always looking for new opportunities to learn and grow in my field.")
    
    st.header("Informasi Pribadi")
    st.subheader("👤 Nama")
    st.write("Bayuzen Ahmad")
    st.subheader("🏠 Alamat")
    st.write("Jl. Contoh Jakarta Selatan No. 123, Jaksel, Negara")
    st.subheader("📧 Email")
    st.write("zen@example.com")
    st.subheader("📞 Telepon")
    st.write("+1234567890")

    # Pendidikan
    st.header("🎓 Pendidikan")
    st.subheader("🎓 Sarjana Teknik Informatika")
    st.write("Universitas ABC, Tahun Lulus: 2020")
    st.subheader("🏫 SMA")
    st.write("SMA XYZ, Tahun Lulus: 2016")

    # Pengalaman Kerja
    st.header("💼 Pengalaman Kerja")
    st.subheader("Software Engineer")
    st.write("Perusahaan ABC, 2020 - Sekarang")
    st.write("Deskripsi pekerjaan")

    # Keahlian
    st.header("🔧 Keahlian")
    st.subheader("🐍 Bahasa Pemrograman")
    st.write("- Python")
    st.write("- JavaScript")
    st.subheader("🌐 Pengembangan Web")
    st.write("- HTML/CSS")
    st.write("- Flask")
    st.write("- Django")


if __name__ == '__main__':
    main()
