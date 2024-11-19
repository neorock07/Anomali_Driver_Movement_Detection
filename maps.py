import streamlit as st
import pandas as pd
import math

def calc_bearing(lat1, long1, lat2, long2):
  # Convert latitude and longitude to radians
  lat1 = math.radians(lat1)
  long1 = math.radians(long1)
  lat2 = math.radians(lat2)
  long2 = math.radians(long2)
  

  bearing = math.atan2(
      math.sin(long2 - long1) * math.cos(lat2),
      math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(long2 - long1)
  )
  
  bearing = math.degrees(bearing)
  
  bearing = (bearing + 360) % 360
  
  return bearing

def load_file(file):
    try:
        # Cek apakah file berformat Excel atau CSV
        if file.name.endswith(".csv"):
            df = pd.read_csv(file, delimiter=";")
        elif file.name.endswith(".xlsx"):
            df = pd.read_excel(file)
        else:
            st.error("Format file tidak didukung. Harap unggah file .csv atau .xlsx.")
            return None
        return df
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")
        return None

def calc_range(bear, deviasi):
    delta_min = (bear - (deviasi/2)) % 360
    delta_max = (bear + (deviasi/2)) % 360
    
    return delta_min, delta_max

def check_angle(angle, start, end):
    """
    Memeriksa apakah sudut dalam rentang minimal dan maksimal sudut deviasi.
  
    :param angle: Sudut belokan dari titik 1 ke titik 2.
    :param start: Batas sudut minimum deviasi terhdap arah Utara. 
    :param end: Batas sudut maksimum deviasi terhdap arah Utara.
    :return: True jika angle berada dalam range, False jika tidak.
    """
    
    if start <= end:
        return start <= angle <= end
    else:
        # Jika rentang melintasi 0 derajat
        return angle >= start or angle <= end

def check_anomali(bear_driver, deviasi=240, data=None):
    anomali = []
    for i in range(len(bear_driver)):
        if i > 0:
            d_min, d_max = calc_range(bear_driver[i-1], deviasi)        
            if check_angle(bear_driver[i], d_min, d_max):
                print(f"titik {bear_driver[i]} , {d_min} | {d_max} Normal")
            else:
                print(f"titik {bear_driver[i]} , {d_min} | {d_max} Anomali")
                anomali.append({"index":i})
                # anomali.append({i:bear_driver[i]})
    
    if data is not None and len(anomali) > 0:
        dt_lat = []
        dt_lon = []
        st.write("Anomali pada titik : ")
        for i in anomali:
            index = i['index']
            dt_lat.append(data['lat'][index])
            dt_lon.append(data['lon'][index])
            # st.write(f"{data['lat'][index]}, {data['lon'][index]}")
        dt = pd.DataFrame({
            "lat" : dt_lat, 
            "lon" : dt_lon
        })
        st.dataframe(dt)   
    st.write(f"Score Anomali : {len(anomali)}/{len(bear_driver)} : {len(anomali)/len(bear_driver)}")            
    return anomali
                             

def main():
    
    st.sidebar.title("Upload File untuk Membuat DataFrame")
    st.sidebar.write("Unggah file CSV atau Excel yang memiliki kolom 'lat' dan 'lon'.")
    
    # Komponen upload file
    uploaded_file = st.sidebar.file_uploader("Pilih file CSV atau Excel", type=["csv", "xlsx"])

    if uploaded_file is not None:
        df = load_file(uploaded_file)

        if df is not None:
            
            # Cek apakah kolom "lat" dan "lon" ada
            if {"lat", "lon"}.issubset(df.columns):
                bearing_driver2 = []
                for i in range(df.shape[0]):
                    # if i == 0:
                    #     continue
                    if i < df.shape[0] -1:
                        bearing_driver2.append(calc_bearing(
                            df['lat'][i], 
                            df['lon'][i], 
                            df['lat'][i+1], 
                            df['lon'][i+1], 
                        ))
                
                st.dataframe(df)
                result = check_anomali(bearing_driver2, 240, df)
                st.map(df, size=2, color="#fff")
            else:
                st.error("File tidak memiliki kolom 'lat' dan 'lon'.")
main()

# dt = pd.DataFrame(
#     {
#         "lat" : [
                # -7.586164, 
                #  -7.585760,
                #  -7.585165,
                #  -7.584654,
                #  -7.583080,
                #  -7.582601,
                #  -7.582946,
                #  -7.583302,
                #  -7.584080,
                #  -7.585202,
                #  -7.586034,
                #  -7.586839,
                #  -7.586758,
                #  -7.586580
#                  ],
#         "lon":[
            # 110.801455,
            # 110.799953,
            # 110.799352,
            # 110.799524,
            # 110.799985,
            # 110.800328,
            # 110.801612,
            # 110.802971,
            # 110.805470,
            # 110.805068,
            # 110.804775,
            # 110.803959,
            # 110.803619,
            # 110.803030
#         ]
#     })
