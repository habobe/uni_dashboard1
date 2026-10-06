from flask import Flask, render_template, jsonify
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1111",
        database="universitysystem"
    )
    return connection

@app.route('/')
def home():
    return render_template('index.html')

# الـ API الشامل لجلب بيانات الطالب وإضافة الأندية والكورسات والكتب والأبحاث
@app.route('/get_student/<int:student_id>', methods=['GET'])
def get_student(student_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        query = """
            SELECT s.student_id, s.student_name, s.Birthdate, s.email, s.card_NO, s.state, s.academic_level, s.enrollment_date,
                   p.phone_number,
                   sc.grade, sc.score, sc.attendance_hours,
                   c.course_name,
                   b.Book_name, sb.Borrow_Date, sb.Return_Date,
                   rp.Project_Name,
                   cl.club_name
            FROM student_university_id s
            LEFT JOIN student_phone p ON s.student_id = p.student_id
            LEFT JOIN student_card card ON s.card_NO = card.card_NO
            LEFT JOIN student_course sc ON s.student_id = sc.student_id
            LEFT JOIN courses c ON sc.course_id = c.course_id
            LEFT JOIN student_book sb ON s.student_id = sb.student_id
            LEFT JOIN book b ON sb.Book_id = b.Book_id
            LEFT JOIN research_project rp ON s.student_id = rp.student_id
            LEFT JOIN student_club s_cl ON s.student_id = s_cl.student_id
            LEFT JOIN club cl ON s_cl.club_id = cl.club_id
            WHERE s.student_id = %s
        """
        cursor.execute(query, (student_id,))
        results = cursor.fetchall()
        
        if results:
            student_data = {
                "student_id": results[0]["student_id"],
                "name": results[0]["student_name"],
                "birthdate": str(results[0]["Birthdate"]),
                "email": results[0]["email"],
                "state": results[0]["state"],
                "academic_level": results[0]["academic_level"],
                "enrollment_date": str(results[0]["enrollment_date"]),
                "phone": results[0]["phone_number"],
                "card_no": results[0]["card_NO"],
                "courses": list(set([row["course_name"] for row in results if row["course_name"]])),
                "books": list(set([row["Book_name"] for row in results if row["Book_name"]])),
                "research_projects": list(set([row["Project_Name"] for row in results if row["Project_Name"]])),
                "clubs": list(set([row["club_name"] for row in results if row["club_name"]]))
            }
            return jsonify(student_data)
        else:
            return jsonify({"error": "عذراً، لم يتم العثور على طالب بهذا الرقم التعريفي!"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)