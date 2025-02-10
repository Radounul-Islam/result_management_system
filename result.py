
import csv

class Result:

    marks = dict()
    results = dict()

    def __init__(self, mark: dict):
        student_id = mark['id']
        mark.pop('id')
        Result.marks[student_id] = mark

    @classmethod
    def instenciate_from_csv(cls, results_csv):
        with open(results_csv, 'r') as results:
            reader = csv.DictReader(results)
            results = list(reader)
            for result in results:
                Result(result)
    

    @classmethod
    def caluclate_results(cls) -> None:
            for id in Result.marks:
                individual_mark = cls.get_individual_mark(id)
                Result.results[id] = cls.calculate_individual_gpa(individual_mark)

                

    @classmethod
    def calculate_individual_gpa(cls, mark: dict, credit_hours: dict = None):
        individual_result = {}
        for subject in mark:
            individual_result[subject] = cls.calculate_gpa_and_grade(mark[subject])
        
        sum_of_gpa_product_credit = 0.0

        if credit_hours == None:
            total_credit_hours = len(mark)
            for subject  in mark:
                sum_of_gpa_product_credit += individual_result[subject][0]
    
        
        else:

            total_credit_hours = sum(credit_hours.values())

            for subject in credit_hours:
                sum_of_gpa_product_credit += individual_result[subject][0] * credit_hours[subject]
        

        total_gpa = sum_of_gpa_product_credit / total_credit_hours

        individual_result["tatal_gpa"] = round(total_gpa, 2)

        return individual_result
        
        
    @classmethod
    def get_individual_mark(cls, id: str) -> dict:
        individual_mark = {}

        for subject in Result.marks[id]:
            if Result.marks[id][subject] == None:
                individual_mark[subject] = 0.0
            
            else:
                individual_mark[subject] = int(Result.marks[id][subject])
        
        return individual_mark
    
    @classmethod      
    def calculate_gpa_and_grade(cls, mark):

        if mark >= 80:
            return 4.0, "A+"
        elif 75 <= mark < 80 :
            return 3.75, "A"
        elif 70 <= mark < 75:
            return 3.5, "A-"
        elif 65 <= mark < 70:
            return 3.25, "B+"
        elif 60 <= mark < 65:
            return 3.00, "B"
        elif 55 <= mark < 60:
            return 2.75, "B-"
        elif 50 <= mark < 55:
            return 2.5, "C+"
        elif 45 <= mark < 50:
            return 2.25, "C"
        elif 40 <= mark < 45:
            return 2, 'D'
        else:
            return 0.0, "F"
        


def main() -> None:
    Result.instenciate_from_csv('results.csv')
    
    Result.caluclate_results()

    

        


   
    
if __name__ == '__main__':
    main()





    

        

    