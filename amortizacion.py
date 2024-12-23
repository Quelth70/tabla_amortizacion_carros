from collections import defaultdict
import datetime
from dateutil.relativedelta import relativedelta


def amort_table(cost, down, interest, years, insurance, accesories, extras, **kwargs):
    is_life_insurance = kwargs.get("is_life_insurance")
    if is_life_insurance == "Si":
        is_life_insurance = True
    else:
        is_life_insurance = False
    life_insurance = kwargs.get("life_insurance")

    monthly_interest = interest / 1200
    monthly_interest_with_vat = monthly_interest * 1.16
    months = years * 12
    financed_car = cost - down

    total_financed = financed_car + accesories + extras 

    M = round((total_financed * monthly_interest_with_vat * (1 + monthly_interest_with_vat)**(months)) / ((1 + monthly_interest_with_vat)**(months) - 1),2)
    M_insurance = round((insurance * monthly_interest_with_vat * (1 + monthly_interest_with_vat)**(12)) / ((1 + monthly_interest_with_vat)**(12) - 1),2)

    principal_car_left = financed_car + accesories + extras
    ins_left = insurance

    current_date = datetime.date.today()

    table = defaultdict(list)
    for i in range(months + 1):
        pay_date = current_date.replace(day = 1) + relativedelta(months = i + 1)
        pay_date = pay_date.strftime("%d-%m-%Y")
    
        if i == 0:
            table["No. de Pago"].append(i)
            table["Capital Restante"].append(principal_car_left + ins_left)
            table["Capital Amort. Vehiculo"].append(i)
            table["Capital Amort. Seguro"].append(i)
            table["Intereses del Periodo"].append(i)
            table["IVA de los Intereses"].append(i)

            if is_life_insurance:
                table["Seguro de Vida"].append(i)

            table["Mensualidad Total"].append(i)
        
        elif not (i%12 == 0) or i == 60:
            car_int = round(principal_car_left * monthly_interest, 2)
            ins_int = round(ins_left * monthly_interest,2)
            car_ins_vat = round(car_int * .16,2)
            ins_int_vat = round(ins_int * .16,2)
            ins_principal = M_insurance - ins_int - ins_int_vat
            car_principal = M - car_int - car_ins_vat
            int_vat = round((car_int + ins_int) * .16,2)

            principal_car_left -= car_principal
            ins_left -= ins_principal

            table["No. de Pago"].append(i)
            table["Capital Restante"].append(principal_car_left + ins_left)
            table["Capital Amort. Vehiculo"].append(car_principal)
            table["Capital Amort. Seguro"].append(ins_principal)
            table["Intereses del Periodo"].append(car_int + ins_int)
            table["IVA de los Intereses"].append(int_vat)

            if is_life_insurance:
                table["Seguro de Vida"].append(life_insurance)
                table["Mensualidad Total"].append(M + M_insurance + life_insurance)
            else:
                table["Mensualidad Total"].append(M + M_insurance)

        else:
            car_int = round(principal_car_left * monthly_interest, 2)
            ins_int = round(ins_left * monthly_interest, 2)
            car_ins_vat = round(car_int * .16,2)
            ins_int_vat = round(ins_int * .16,2)
            ins_principal = M_insurance - ins_int - ins_int_vat
            car_principal = M - car_int - car_ins_vat
            int_vat = round((car_int + ins_int) * .16,2)

            table["No. de Pago"].append(i)
            table["Capital Amort. Vehiculo"].append(car_principal)
            table["Capital Amort. Seguro"].append(ins_principal)
            table["Intereses del Periodo"].append(car_int + ins_int)
            table["IVA de los Intereses"].append(int_vat)
            
            if is_life_insurance:
                table["Seguro de Vida"].append(life_insurance)
                table["Mensualidad Total"].append(M + M_insurance + life_insurance)
            else:
                table["Mensualidad Total"].append(M + M_insurance)

            principal_car_left -= car_principal
            ins_left = insurance

            table["Capital Restante"].append(principal_car_left + ins_left)

    return table


def first_year_free_amort_table(cost, down, interest, years, insurance, accesories, extras, **kwargs):
    is_life_insurance = kwargs.get("is_life_insurance")
    if is_life_insurance == "Si":
        is_life_insurance = True
    else:
        is_life_insurance = False
    life_insurance_1 = kwargs.get("life_insurance_1")
    life_insurance_2 = kwargs.get("life_insurance_2")

    monthly_interest = interest / 1200
    monthly_interest_with_vat = monthly_interest * 1.16
    months = years * 12
    financed_car = cost - down

    total_financed = financed_car + accesories + extras

    M = round((total_financed * monthly_interest_with_vat * (1 + monthly_interest_with_vat)**(months)) / ((1 + monthly_interest_with_vat)**(months) - 1),2)
    M_insurance = round((insurance * monthly_interest_with_vat * (1 + monthly_interest_with_vat)**(12)) / ((1 + monthly_interest_with_vat)**(12) - 1),2)

    principal_car_left = financed_car + accesories + extras
    ins_left = 0

    current_date = datetime.date.today()

    table = defaultdict(list)
    for i in range(months + 1):
        pay_date = current_date.replace(day = 1) + relativedelta(months = i + 1)
        pay_date = pay_date.strftime("%d-%m-%Y")

        if i == 0:
            table["No. de Pago"].append(i)
            table["Capital Restante"].append(principal_car_left + ins_left)
            table["Capital Amort. Vehiculo"].append(i)
            table["Capital Amort. Seguro"].append(i)
            table["Intereses del Periodo"].append(i)
            table["IVA de los Intereses"].append(i)

            if is_life_insurance:
                table["Seguro de Vida"].append(i)

            table["Mensualidad Total"].append(i)

        elif i <= 12:
            car_int = round(principal_car_left * monthly_interest, 2)
            car_ins_vat = round(car_int * .16,2)

            car_principal = M - car_int - car_ins_vat

            principal_car_left -= car_principal

            table["No. de Pago"].append(i)
            table["Capital Restante"].append(principal_car_left + ins_left)
            table["Capital Amort. Vehiculo"].append(car_principal)
            table["Capital Amort. Seguro"].append(0)
            table["Intereses del Periodo"].append(car_int)
            table["IVA de los Intereses"].append(car_ins_vat)

            if is_life_insurance:
                table["Seguro de Vida"].append(life_insurance_1)
                table["Mensualidad Total"].append(M + life_insurance_1)
            else:
                table["Mensualidad Total"].append(M)

            ins_left = insurance
        
        elif not (i%12 == 0) or i == 60:
            car_int = round(principal_car_left * monthly_interest, 2)
            ins_int = round(ins_left * monthly_interest,2)
            car_ins_vat = round(car_int * .16,2)
            ins_int_vat = round(ins_int * .16,2)
            ins_principal = M_insurance - ins_int - ins_int_vat
            car_principal = M - car_int - car_ins_vat
            int_vat = round((car_int + ins_int) * .16,2)

            principal_car_left -= car_principal
            ins_left -= ins_principal

            table["No. de Pago"].append(i)
            table["Capital Restante"].append(principal_car_left + ins_left)
            table["Capital Amort. Vehiculo"].append(car_principal)
            table["Capital Amort. Seguro"].append(ins_principal)
            table["Intereses del Periodo"].append(car_int + ins_int)
            table["IVA de los Intereses"].append(int_vat)

            if is_life_insurance:
                table["Seguro de Vida"].append(life_insurance_2)
                table["Mensualidad Total"].append(M + M_insurance + life_insurance_2)
            else:
                table["Mensualidad Total"].append(M + M_insurance)

        else:
            car_int = round(principal_car_left * monthly_interest, 2)
            ins_int = round(ins_left * monthly_interest, 2)
            car_ins_vat = round(car_int * .16,2)
            ins_int_vat = round(ins_int * .16,2)
            ins_principal = M_insurance - ins_int - ins_int_vat
            car_principal = M - car_int - car_ins_vat
            int_vat = round((car_int + ins_int) * .16,2)

            table["No. de Pago"].append(i)
            table["Capital Amort. Vehiculo"].append(car_principal)
            table["Capital Amort. Seguro"].append(ins_principal)
            table["Intereses del Periodo"].append(car_int + ins_int)
            table["IVA de los Intereses"].append(int_vat)
            
            if is_life_insurance:
                table["Seguro de Vida"].append(life_insurance_2)
                table["Mensualidad Total"].append(M + M_insurance + life_insurance_2)
            else:
                table["Mensualidad Total"].append(M + M_insurance)

            principal_car_left -= car_principal
            ins_left = insurance

            table["Capital Restante"].append(principal_car_left + ins_left)

    return table
