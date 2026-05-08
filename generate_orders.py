import pandas as pd
import random
from datetime import datetime, timedelta

def generate_orders():
    # 시드 지정
    random.seed(42)

    branches = []
    branch_id = 1

    for _ in range(30):
        boxes = random.randint(180, 200)
        branches.append({"branch_id": branch_id, "type": "A", "boxes": boxes})
        branch_id += 1

    for _ in range(20):
        boxes = random.randint(120, 150)
        branches.append({"branch_id": branch_id, "type": "B", "boxes": boxes})
        branch_id += 1

    for _ in range(10):
        boxes = random.randint(30, 80)
        branches.append({"branch_id": branch_id, "type": "C", "boxes": boxes})
        branch_id += 1

    data = []
    box_id_global = 1
    
    # 시뮬레이션 시작 시간을 2026년 4월 1일 00시 00분 00초로 설정
    current_time = datetime(2026, 4, 1, 0, 0, 0)

    # for b in branches:
    #     b_id = b["branch_id"]
    #     b_type = b["type"]
    #     num_boxes = b["boxes"]
        
    #     for _ in range(num_boxes):
    #         has_S = random.random() < 0.50
    #         has_A = random.random() < 0.50
    #         has_B = random.random() < 0.30
    #         has_C = random.random() < 0.05
            
    #         # 확률 계산 후 하나의 등급도 선택되지 않은 경우 S등급이 포함된 것으로 처리
    #         if not (has_S or has_A or has_B or has_C):
    #             has_S = True
                
    #         s_sku = random.randint(1, 4) if has_S else 0
    #         s_qty = sum(random.randint(1, 20) for _ in range(s_sku)) if has_S else 0
            
    #         a_sku = random.randint(1, 4) if has_A else 0
    #         a_qty = sum(random.randint(1, 20) for _ in range(a_sku)) if has_A else 0
            
    #         b_sku = random.randint(1, 4) if has_B else 0
    #         b_qty = sum(random.randint(1, 20) for _ in range(b_sku)) if has_B else 0
            
    #         c_sku = random.randint(1, 4) if has_C else 0
    #         c_qty = sum(random.randint(1, 20) for _ in range(c_sku)) if has_C else 0
            
    #         data.append({
    #             # 엑셀과 호환되는 Datetime 형식으로 저장
    #             "Arrival_Time": current_time,
    #             "Box_ID": box_id_global,
    #             "Branch_ID": b_id,
    #             "Branch_Type": b_type,
    #             "S_SKU_Cnt": s_sku,
    #             "S_Qty": s_qty,
    #             "A_SKU_Cnt": a_sku,
    #             "A_Qty": a_qty,
    #             "B_SKU_Cnt": b_sku,
    #             "B_Qty": b_qty,
    #             "C_SKU_Cnt": c_sku,
    #             "C_Qty": c_qty
    #         })
    #         box_id_global += 1
            
    #         # 기계 3대가 분당 90개를 처리하므로, 약 0.66초 간격으로 스폰되도록 시간 증가
    #         current_time += timedelta(seconds=0.666)

    # df = pd.DataFrame(data)
    
    # output_path = "c:/202444085_Assemble/simulation/simulation_orders.xlsx"
    # df.to_excel(output_path, index=False)
    
    # print("✅ 완료: 시간표(Arrival_Time)를 날짜형식(Date)으로 수정했습니다!")

    max_boxes = max(b["boxes"] for b in branches)
    box_counters = [0] * len(branches)  # 각 branch별 생성된 박스 수 추적
    for i in range(max_boxes):
        for j, b in enumerate(branches):
            if box_counters[j] >= b["boxes"]:
                continue  # 이 branch는 이미 다 생성됨
            b_id = b["branch_id"]
            b_type = b["type"]
            has_S = random.random() < 0.50
            has_A = random.random() < 0.50
            has_B = random.random() < 0.30
            has_C = random.random() < 0.05
            if not (has_S or has_A or has_B or has_C):
                has_S = True
            s_sku = random.randint(1, 4) if has_S else 0
            s_qty = sum(random.randint(1, 20) for _ in range(s_sku)) if has_S else 0
            a_sku = random.randint(1, 4) if has_A else 0
            a_qty = sum(random.randint(1, 20) for _ in range(a_sku)) if has_A else 0
            b_sku = random.randint(1, 4) if has_B else 0
            b_qty = sum(random.randint(1, 20) for _ in range(b_sku)) if has_B else 0
            c_sku = random.randint(1, 4) if has_C else 0
            c_qty = sum(random.randint(1, 20) for _ in range(c_sku)) if has_C else 0
            data.append({
                "Arrival_Time": current_time,
                "Box_ID": box_id_global,
                "Branch_ID": b_id,
                "Branch_Type": b_type,
                "S_SKU_Cnt": s_sku, "S_Qty": s_qty,
                "A_SKU_Cnt": a_sku, "A_Qty": a_qty,
                "B_SKU_Cnt": b_sku, "B_Qty": b_qty,
                "C_SKU_Cnt": c_sku, "C_Qty": c_qty
            })
            box_id_global += 1
            current_time += timedelta(seconds=0.666)
            box_counters[j] += 1

    df = pd.DataFrame(data)
    output_path = "simulation_orders.xlsx"
    df.to_excel(output_path, index=False)
    print(f"✅ 완료: {len(data)}개 박스, 라운드 로빈 투입 순서로 생성")

if __name__ == "__main__":
    generate_orders()
