import numpy as np
import sys
import time

# Гравитационная постоянная
G = 6.6743e-11

class Planet:
    def __init__(self, name, mass, r, v):
        self.name = name
        self.mass = float(mass)
        # переводим в numpy массивы для быстрых векторов
        self.r = np.array(r, dtype=np.float64)
        self.v = np.array(v, dtype=np.float64)

def calc_gravity(bodies):
    # TODO: переписать этот кусок на матричные вычисления (без циклов). 
    # Питон дико тупит на вложенных циклах, если тел больше 100, но для 4-х сойдет.
    n = len(bodies)
    acc = np.zeros((n, 3))
    
    for i in range(n):
        for j in range(n):
            if i == j: 
                continue
                
            vec = bodies[j].r - bodies[i].r
            dist = np.linalg.norm(vec)
            
            # костыль от деления на ноль, если объекты влетят друг в друга
            if dist < 1e3:
                continue 
                
            # a = F/m = G * M / r^2
            acc[i] += G * bodies[j].mass * vec / (dist**3)
            
    return acc

def run_sim():
    print("Инициализация движка...")
    
    # Массы и примерные координаты (данные брал из вики, могут чуть отличаться)
    # Координаты в метрах, скорость в м/с
    bodies = [
        Planet("Sun", 1.989e30, [0, 0, 0], [0, 0, 0]),
        Planet("Earth", 5.972e24, [1.496e11, 0, 0], [0, 29780, 0]),
        Planet("Jupiter", 1.898e27, [7.785e11, 0, 0], [0, 13070, 0]),
        
        # Вояджер стартует около Земли с лютой скоростью для гравитационного маневра
        Planet("Voyager-1", 722.0, [1.496e11 + 1e7, 0, 0], [0, 42000, 0]) 
    ]

    # Шаг симуляции (1 день = 86400 сек). 
    dt = 24 * 3600  
    years_to_sim = 12 
    days = 365 * years_to_sim 
    
    print(f"Погнали! Симулируем {years_to_sim} лет полета...")
    start_time = time.time()
    
    for step in range(days):
        acc = calc_gravity(bodies)
        
        # Интегрирование методом Эйлера-Кромера 
        # (Можно прикрутить Рунге-Кутту RK4, но лень писать, для портфолио пока так)
        for i, b in enumerate(bodies):
            b.v += acc[i] * dt
            b.r += b.v * dt
            
        # Выводим логи каждый год симуляции
        if step > 0 and step % 365 == 0:
            y = step // 365
            voyager = bodies[3] # хардкод индекса вояджера, надо бы переделать по имени
            dist_au = np.linalg.norm(voyager.r) / 1.496e11
            speed_km = np.linalg.norm(voyager.v) / 1000
            
            print(f"Год {y}: Вояджер отдалился на {dist_au:.2f} a.e. | Скорость: {speed_km:.2f} км/с")

    elapsed = time.time() - start_time
    print(f"\nСимуляция завершена за {elapsed:.2f} сек.")
    # print("TODO: Прикрутить matplotlib для отрисовки графиков орбит")

if __name__ == '__main__':
    try:
        run_sim()
    except KeyboardInterrupt:
        print("\nРабота прервана пользователем. Выходим...")
        sys.exit(0)
