import math

def calc_bearing(lat1, long1, lat2, long2):
  """
  Fungsi untuk menghitung besar sudut bearing antar dua titik koordinat.
  
  :param lat1 (float): latitude data pertama.
  :param long1 (float): longitude data pertama.
  :param lat2 (float): latitude data kedua.
  :param lon2 (float): longitude data kedua.
  :return bearing (float): besar sudut bearing.
  """
  
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

def calc_range(bear, deviasi):
    """
    Fungsi untuk menghitung range sudut deviasi terhadap arah Utara, 
    karena sebagai pengamat titik 0 derajat ada di Utara.
    
    :param bear (list): list sudut bearing driver.
    :param deviasi (int): besar sudut deviasi.
    :return delta_min (int): derajat sudut minimum deviasi terhadap Utara.
    :return delta_max (int): derajat sudut maximum deviasi terhadap Utara.
    """
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
        return angle >= start or angle <= end
    

def check_anomali(bear_driver, deviasi, koordinat:list):
    """
    Memeriksa apakah titik data termasuk Normal atau Anomali.
    
    :param bear_driver (list): List sudut bearing driver.
    :param deviasi (int|float): besar sudut deviasi
    :param koordinat (list): koordinat driver
    """
    anomali = []
    for i in range(len(bear_driver)):
        if i > 0:
            d_min, d_max = calc_range(bear_driver[i-1], deviasi)        
            if check_angle(bear_driver[i], d_min, d_max):
                print(f"titik {koordinat[i]} angle: {bear_driver[i]}, {d_min} | {d_max} Normal")
            else:
                print(f"titik {koordinat[i]} angle: {bear_driver[i]}, {d_min} | {d_max} Anomali")
                anomali.append(bear_driver[i])
    print(f"Score Anomali : {len(anomali)}/{len(bear_driver)} : {len(anomali)/len(bear_driver)}")            

 
def get_bearing(koordinat:list):
    """
    Menghitung sudut bearing antar titik koordinat.
    
    :param koordinat (list): koordiant driver.
    :return bearing_driver (list): list sudut bearing jalur driver.
    """
    bearing_driver = []
    for i in range(len(koordinat)):
        if i < len(koordinat) -1:
            bearing_driver.append(calc_bearing(
                koordinat[i][0], 
                koordinat[i][1], 
                koordinat[i+1][0], 
                koordinat[i+1][1], 
            ))
    return bearing_driver        

bear = [
    [-7.586164, 110.801455],
    [-7.585760, 110.799953],
    [-7.585165, 110.799352],
    [-7.584654, 110.799524],
    [-7.583080, 110.799985],
    [-7.582601, 110.800328],
    [-7.582946, 110.801612],
    [-7.583302, 110.802971],
    [-7.585202, 110.805068],
    [-7.586034, 110.804775],
    [-7.586839, 110.803959],
    [-7.584080, 110.805470],
    [-7.586758, 110.803619],
    [-7.586580, 110.803030]
]

result_bear = get_bearing(bear)
b_deviasi = 240
check_anomali(result_bear, b_deviasi, bear)             