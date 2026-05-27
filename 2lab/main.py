import math
import matplotlib.pyplot as plt
from functools import reduce
import itertools as it
from typing import Iterator, Tuple, List

Polygon = Tuple[Tuple[float, float], ...]

def side_lengths(poly: Polygon) -> List[float]:
    n = len(poly)
    return [math.dist(poly[i], poly[(i + 1) % n]) for i in range(n)]

def polygon_perimeter(poly: Polygon) -> float:
    return sum(side_lengths(poly))

def polygon_area(poly: Polygon) -> float:
    n = len(poly)
    s = sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))
    return abs(s) / 2.0

def is_convex(poly: Polygon) -> bool:
    n = len(poly)
    if n < 3:
        return False
    signs = []
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        x3, y3 = poly[(i + 2) % n]
        cross = (x2 - x1) * (y3 - y2) - (y2 - y1) * (x3 - x2)
        if cross != 0:
            signs.append(cross > 0)
    return all(signs) or not any(signs)

def point_inside_polygon(point: Tuple[float, float], poly: Polygon) -> bool:
    x, y = point
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        intersect = ((y1 > y) != (y2 > y)) and (
            x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-9) + x1
        )
        if intersect:
            inside = not inside
    return inside

def polygons_intersect(poly1: Polygon, poly2: Polygon) -> bool:
    for p in poly1:
        if point_inside_polygon(p, poly2): return True
    for p in poly2:
        if point_inside_polygon(p, poly1): return True
    return False


# пункт 2
def gen_rectangle(width: float = 1.0, height: float = 0.6, gap: float = 0.2) -> Iterator[Polygon]:
    return map(lambda i: ((i * (width + gap), 0), 
                          (i * (width + gap) + width, 0), 
                          (i * (width + gap) + width, height), 
                          (i * (width + gap), height)), it.count())

def gen_triangle(base: float = 1.0, height: float = 0.8, gap: float = 0.2) -> Iterator[Polygon]:
    return map(lambda i: ((i * (base + gap), 0), 
                          (i * (base + gap) + base, 0), 
                          (i * (base + gap) + base / 2, height)), it.count())

def gen_hexagon(radius: float = 0.5, gap: float = 0.2) -> Iterator[Polygon]:
    def make_hex(offset_x):
        return tuple((offset_x + radius * math.cos(math.radians(60 * i)), 
                      radius * math.sin(math.radians(60 * i))) for i in range(6))
    return map(lambda i: make_hex(i * (2 * radius + gap)), it.count())

#пункт 3
def tr_translate(poly: Polygon, dx: float, dy: float) -> Polygon:
    return tuple((x + dx, y + dy) for x, y in poly)

def tr_rotate(poly: Polygon, angle_deg: float, center: Tuple[float, float] = (0, 0)) -> Polygon:
    rad = math.radians(angle_deg)
    c, s = math.cos(rad), math.sin(rad)
    cx, cy = center
    return tuple(((x - cx) * c - (y - cy) * s + cx, (x - cx) * s + (y - cy) * c + cy) for x, y in poly)

def tr_symmetry(poly: Polygon, axis: str = 'x', center: Tuple[float, float] = (0, 0)) -> Polygon:
    cx, cy = center
    if axis == 'x':
        return tuple((x, 2 * cy - y) for x, y in poly)
    elif axis == 'y':
        return tuple((2 * cx - x, y) for x, y in poly)
    else:
        return tuple((2 * cx - x, 2 * cy - y) for x, y in poly)

def tr_homothety(poly: Polygon, k: float, center: Tuple[float, float] = (0, 0)) -> Polygon:
    cx, cy = center
    return tuple((cx + k * (x - cx), cy + k * (y - cy)) for x, y in poly)

#пункт 5
def flt_convex_polygon(poly: Polygon) -> bool:
    return is_convex(poly)

def flt_angle_point(poly: Polygon, point: Tuple[float, float]) -> bool:
    return any(math.isclose(p[0], point[0], abs_tol=1e-5) and math.isclose(p[1], point[1], abs_tol=1e-5) for p in poly)

def flt_square(poly: Polygon, max_area: float) -> bool:
    return polygon_area(poly) < max_area

def flt_short_side(poly: Polygon, max_side: float) -> bool:
    return min(side_lengths(poly)) < max_side

def flt_point_inside(poly: Polygon, point: Tuple[float, float]) -> bool:
    return is_convex(poly) and point_inside_polygon(point, poly)

def flt_polygon_angles_inside(poly: Polygon, other_poly: Polygon) -> bool:
    return is_convex(poly) and any(point_inside_polygon(p, poly) for p in other_poly)

#пункт 8
def agr_origin_nearest(polygons: Iterator[Polygon]) -> Tuple[float, float]:
    all_points = (pt for poly in polygons for pt in poly)
    return reduce(lambda p1, p2: p1 if math.dist(p1, (0, 0)) < math.dist(p2, (0, 0)) else p2, all_points)

def agr_max_side(polygons: Iterator[Polygon]) -> float:
    return reduce(max, map(lambda p: max(side_lengths(p)), polygons))

def agr_min_area(polygons: Iterator[Polygon]) -> float:
    return reduce(min, map(polygon_area, polygons))

def agr_perimeter(polygons: Iterator[Polygon]) -> float:
    return reduce(lambda a, b: a + b, map(polygon_perimeter, polygons), 0.0)

def agr_area(polygons: Iterator[Polygon]) -> float:
    return reduce(lambda a, b: a + b, map(polygon_area, polygons), 0.0)


def draw_polygons(ax, polygons, title="", facecolor='none', edgecolor='black', fill_alpha=1.0):
    for poly in polygons:
        x = [p[0] for p in poly] + [poly[0][0]]
        y = [p[1] for p in poly] + [poly[0][1]]
        ax.plot(x, y, color=edgecolor, linewidth=1.2)
        if facecolor != 'none':
            ax.fill(x, y, alpha=fill_alpha, color=facecolor)
    
    ax.set_title(title, fontsize=10)
    ax.set_aspect('equal')
    ax.axis('off')

def demo_generators():
    print("\n[Пункт 2] Генерация базовых фигур...")
    fig, axs = plt.subplots(3, 1, figsize=(10, 8))
    
    draw_polygons(axs[0], list(it.islice(gen_rectangle(), 7)), "1. Семь непересекающихся прямоугольников в ряд", edgecolor='black')
    draw_polygons(axs[1], list(it.islice(gen_triangle(), 7)), "2. Семь непересекающихся треугольников в ряд", edgecolor='black')
    draw_polygons(axs[2], list(it.islice(gen_hexagon(), 7)), "3. Семь непересекающихся правильных шестиугольников в ряд", edgecolor='black')
    
    for ax in axs:
        ax.axhline(0, color='gray', linewidth=0.5)
        ax.axvline(0, color='gray', linewidth=0.5)
        ax.autoscale()
    plt.tight_layout()
    plt.show()
#пункт 4
def demo_transformations():
    print("\n[Пункт 4] Визуализация трансформаций...")
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    
    #а) Три параллельных ленты
    ax = axs[0, 0]
    row_rects = list(it.islice(gen_rectangle(width=0.8, height=0.4, gap=0.2), 7))
    tilted_row1 = list(map(lambda p: tr_rotate(p, 25), row_rects))
    tilted_row2 = list(map(lambda p: tr_translate(p, -1.0, 1.5), tilted_row1))
    tilted_row3 = list(map(lambda p: tr_translate(p, -2.0, 3.0), tilted_row1))
    draw_polygons(ax, tilted_row1 + tilted_row2 + tilted_row3, "1. Три параллельных ленты под острым углом")
    
    #б) Две пересекающиеся ленты
    ax = axs[0, 1]
    centered_rects = list(map(lambda p: tr_translate(p, -3.5, -0.2), row_rects))
 
    cross1_base = list(map(lambda p: tr_rotate(p, 45), centered_rects))
    cross2_base = list(map(lambda p: tr_rotate(p, -45), centered_rects))
    
    cross1 = list(map(lambda p: tr_translate(p, 4.0, 3.0), cross1_base))
    cross2 = list(map(lambda p: tr_translate(p, 4.0, 3.0), cross2_base))
    
    draw_polygons(ax, cross1 + cross2, "2. Две пересекающиеся ленты не в начале координат")
    ax.plot([4], [3], marker='o', color='red', markersize=4) 
    
    #в)Симметрично отображенные ленты
    ax = axs[1, 0]
    row_tris = list(it.islice(gen_triangle(base=0.8, height=0.8, gap=0.2), 7))
    tris_up = list(map(lambda p: tr_translate(p, 0, 0.2), row_tris))
    tris_down = list(map(lambda p: tr_symmetry(p, axis='x', center=(0,0)), tris_up))
    draw_polygons(ax, tris_up + tris_down, "3. Два симметричных ряда треугольников")
    
    #г) последовательность четырехугольников в разном масштабе
    ax = axs[1, 1]
    
    base_quad = ((1.0, 0.5), (2.0, 1.0), (1.5, 2.25), (0.5, 0.75))
    scales = [1.0, 1.8, 3.0, 4.5]
    quads_q1 = list(map(lambda k: tr_homothety(base_quad, k), scales))
    
    quads_q3 = list(map(lambda p: tr_symmetry(p, axis='origin', center=(0,0)), quads_q1))
    draw_polygons(ax, quads_q1 + quads_q3, "4. Последовательность масштабируемых четырехугольников")
    
    ax.plot([-8, 8], [-4, 4], color='red', linestyle='--', linewidth=0.8, alpha=0.5)
    ax.plot([-8, 8], [-12, 12], color='red', linestyle='--', linewidth=0.8, alpha=0.5)
    
    for r in range(2):
        for c in range(2):
            axs[r, c].axhline(0, color='gray', linewidth=0.5)
            axs[r, c].axvline(0, color='gray', linewidth=0.5)
            axs[r, c].autoscale()
            
    plt.tight_layout()
    plt.show()

def demo_scenario_filters():
    print("\n[Пункт 6] Сценарии применения фильтров...")
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    
    #сценарий 1
    base_trap = ((1, 0.3), (2, 0.6), (2, -0.6), (1, -0.3))
    quads_infinite = map(lambda k: tr_homothety(base_trap, k), it.count(1, 0.5))
    six_figures = list(it.islice(quads_infinite, 6))
    
    print(f"Сценарий 1: Взято {len(six_figures)} фигур.")
    draw_polygons(axs[0], six_figures, "Сценарий 1: 6 фигур", edgecolor='blue', facecolor='lightblue', fill_alpha=0.3)

    #сценарий 2
    rects = list(it.islice(gen_rectangle(width=0.5, height=2.0, gap=0.1), 15))
    short_rects = list(it.islice(filter(lambda p: flt_short_side(p, 0.6), rects), 4))
    
    print(f"\nСценарий 2: Отфильтровано {len(short_rects)} фигур (короткая сторона < 0.6):")
    for i, p in enumerate(short_rects):
        sides = [round(s, 2) for s in side_lengths(p)]
        print(f"  Фигура {i+1}: стороны={sides}, площадь={polygon_area(p):.2f}")
    
    draw_polygons(axs[1], short_rects, "Сценарий 2: Короткая сторона", edgecolor='green', facecolor='lightgreen', fill_alpha=0.4)
    
    #сценарий 3
    mixed_polys = [((i * 0.4, 0), (i * 0.4 + 1.0, 0), (i * 0.4 + 1.0, 1.0), (i * 0.4, 1.0)) for i in range(15)]
    non_intersecting = reduce(
        lambda acc, poly: acc if any(polygons_intersect(poly, a) for a in acc) else acc + [poly], 
        mixed_polys, 
        []
    )
    
    print(f"\nСценарий 3: Из 15 фигур осталось {len(non_intersecting)} непересекающихся.")
    draw_polygons(axs[2], non_intersecting, "Сценарий 3: Без пересечений", edgecolor='red', facecolor='salmon', fill_alpha=0.5)

    for ax in axs:
        ax.axhline(0, color='gray', linewidth=0.5)
        ax.axvline(0, color='gray', linewidth=0.5)
        ax.autoscale()
        
    plt.tight_layout()
    plt.show()
#главное меню
def main_menu():
    polygons = []
    
    while True:
        print("МЕНЮ")
        print("1. Добавить полигон")
        print("2. Показать текущие полигоны")
        print("3. Очистить память")
        print("4. Агрегирующие функции (Доп. задание 5 - Пункт 8)")
        print("5. Пункт 2: Генераторы бесконечных последовательностей")
        print("6. Пункт 4: Визуализация трансформаций")
        print("7. Пункт 6: Сценарии фильтров")
        print("0. Выход")
        
        choice = input("Выберите пункт: ").strip()
        
        if choice == '1':
            n = int(input("Количество вершин: "))
            points = tuple((float(input(f"x{i+1}: ")), float(input(f"y{i+1}: "))) for i in range(n))
            polygons.append(points)
            print(f"Полигон добавлен. Всего: {len(polygons)}")
            
        elif choice == '2':
            if polygons:
                fig, ax = plt.subplots(figsize=(6,6))
                draw_polygons(ax, polygons, f"Ваши полигоны ({len(polygons)} шт.)", edgecolor='blue')
                plt.show()
            else:
                print("Нет полигонов")
                
        elif choice == '3':
            polygons.clear()
            print("Очищено")
            
        elif choice == '4':
            if not polygons:
                print("Добавьте полигоны!")
                continue
            try:
                print(f"Ближайшая к началу координат вершина: {agr_origin_nearest(iter(polygons))}")
                print(f"Максимальная длина стороны: {agr_max_side(iter(polygons)):.3f}")
                print(f"Минимальная площадь: {agr_min_area(iter(polygons)):.3f}")
                print(f"Суммарный периметр: {agr_perimeter(iter(polygons)):.3f}")
                print(f"Суммарная площадь: {agr_area(iter(polygons)):.3f}")
            except ValueError as e:
                print(f"Ошибка агрегации: {e}")
                
        elif choice == '5':
            demo_generators()
        elif choice == '6':
            demo_transformations()
        elif choice == '7':
            demo_scenario_filters()
        elif choice == '0':
            break
        else:
            print("Неверный ввод")

if __name__ == "__main__":
    main_menu()
