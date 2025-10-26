from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Temporary in-memory database
students = [
    {"id": 1, "name": "Emily Pajarpa", "grade": 10, "section": "Stallman"},
    {"id": 2, "name": "John Doe", "grade": 9, "section": "Torvalds"},
]

# -----------------------
# HTML FRONTEND (FINAL ENHANCED DESIGN WITH PROPER TABLE SPACING)
# -----------------------
html_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Student Information Management System</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #e0ecff, #f5f9ff);
            margin: 0;
            padding: 0;
            color: #333;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        header {
            background: linear-gradient(135deg, #004aad, #0073ff);
            color: white;
            padding: 25px 0;
            text-align: center;
            box-shadow: 0 3px 10px rgba(0,0,0,0.2);
        }
        h1 {
            margin: 0;
            font-size: 2em;
        }
        .container {
            width: 90%;
            max-width: 950px;
            margin: 30px auto;
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            flex-grow: 1;
        }
        .form-section {
            background: #f8faff;
            border: 1px solid #dde7ff;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 25px;
        }
        input {
            padding: 10px;
            margin: 8px 5px;
            border: 1px solid #ccc;
            border-radius: 6px;
            width: 200px;
            font-size: 14px;
        }
        .btn {
            padding: 10px 15px;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            cursor: pointer;
            background-color: #004aad;
            color: white;
            transition: all 0.2s ease-in-out;
        }
        .btn:hover {
            background-color: #003580;
            transform: scale(1.05);
        }
        .search-bar {
            margin: 20px 0;
        }
        .search-bar input {
            width: 100%;
            padding: 12px;
            border: 1px solid #ccc;
            border-radius: 6px;
            font-size: 14px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 10px;
            table-layout: fixed; /* even distribution */
        }
        th, td {
            text-align: left;
            padding: 12px 15px;
            border-bottom: 1px solid #ddd;
            word-wrap: break-word;
        }
        th {
            background-color: #004aad;
            color: white;
            text-transform: uppercase;
        }
        /* Column width control */
        th:nth-child(1), td:nth-child(1) { width: 10%; text-align: center; }
        th:nth-child(2), td:nth-child(2) { width: 30%; }
        th:nth-child(3), td:nth-child(3) { width: 15%; text-align: center; }
        th:nth-child(4), td:nth-child(4) { width: 20%; text-align: center; }
        th:nth-child(5), td:nth-child(5) { width: 25%; text-align: center; }

        tr:hover {
            background-color: #f1f4ff;
        }
        footer {
            text-align: center;
            padding: 15px;
            margin-top: auto;
            background: #004aad;
            color: white;
        }
        .button-group {
            display: inline-flex;
            gap: 8px;
        }
        .action-buttons {
            display: flex;
            justify-content: center;
            gap: 10px;
        }
        @media (max-width: 600px) {
            input { width: 100%; }
            table, th, td { font-size: 13px; }
            .action-buttons { flex-direction: column; gap: 5px; }
        }
    </style>
</head>
<body>
    <header>
        <h1>Student Information Management System</h1>
    </header>

    <div class="container">

        <div class="form-section">
            <h3>Add / Edit Student</h3>
            <input type="hidden" id="studentId">
            <input type="text" id="name" placeholder="Student Name">
            <input type="number" id="grade" placeholder="Grade Level">
            <input type="text" id="section" placeholder="Section">
            <div class="button-group">
                <button class="btn" onclick="addOrUpdateStudent()">💾 Save</button>
                <button class="btn" onclick="clearForm()">🧹 Clear</button>
            </div>
        </div>

        <div class="search-bar">
            <input type="text" id="searchBox" placeholder="🔍 Search by name..." onkeyup="filterStudents()">
        </div>

        <table>
            <thead>
                <tr>
                    <th>ID</th><th>Name</th><th>Grade</th><th>Section</th><th>Actions</th>
                </tr>
            </thead>
            <tbody id="studentTable"></tbody>
        </table>

    </div>

    <footer>
        &copy; 2025 Student Management System | Designed by Emily Pajarpa
    </footer>

    <script>
        async function fetchStudents() {
            const res = await fetch('/students');
            const data = await res.json();
            renderTable(data);
        }

        function renderTable(data) {
            const table = document.getElementById('studentTable');
            table.innerHTML = '';
            data.forEach(s => {
                table.innerHTML += `
                    <tr>
                        <td>${s.id}</td>
                        <td>${s.name}</td>
                        <td>${s.grade}</td>
                        <td>${s.section}</td>
                        <td>
                            <div class="action-buttons">
                                <button class="btn" onclick="editStudent(${s.id})">✏️ Edit</button>
                                <button class="btn" onclick="deleteStudent(${s.id})">🗑️ Delete</button>
                            </div>
                        </td>
                    </tr>
                `;
            });
        }

        async function addOrUpdateStudent() {
            const id = document.getElementById('studentId').value;
            const name = document.getElementById('name').value.trim();
            const grade = document.getElementById('grade').value;
            const section = document.getElementById('section').value.trim();

            if (!name || !grade || !section) {
                alert("⚠️ Please fill all fields before saving!");
                return;
            }

            const studentData = { name, grade: parseInt(grade), section };

            if (id) {
                await fetch(`/students/${id}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(studentData)
                });
            } else {
                await fetch('/students', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(studentData)
                });
            }

            clearForm();
            fetchStudents();
        }

        async function editStudent(id) {
            const res = await fetch(`/students/${id}`);
            const s = await res.json();
            document.getElementById('studentId').value = s.id;
            document.getElementById('name').value = s.name;
            document.getElementById('grade').value = s.grade;
            document.getElementById('section').value = s.section;
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        async function deleteStudent(id) {
            if (!confirm("Are you sure you want to delete this student?")) return;
            await fetch(`/students/${id}`, { method: 'DELETE' });
            fetchStudents();
        }

        function clearForm() {
            document.getElementById('studentId').value = '';
            document.getElementById('name').value = '';
            document.getElementById('grade').value = '';
            document.getElementById('section').value = '';
        }

        async function filterStudents() {
            const searchValue = document.getElementById('searchBox').value.toLowerCase();
            const res = await fetch('/students');
            const data = await res.json();
            const filtered = data.filter(s => s.name.toLowerCase().includes(searchValue));
            renderTable(filtered);
        }

        fetchStudents();
    </script>
</body>
</html>
"""

# -----------------------
# BACKEND API ROUTES
# -----------------------

@app.route('/')
def home():
    return render_template_string(html_page)

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if student:
        return jsonify(student)
    return jsonify({"message": "Student not found"}), 404

@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    if not data or not all(k in data for k in ("name", "grade", "section")):
        return jsonify({"message": "Invalid input"}), 400

    new_id = max([s["id"] for s in students], default=0) + 1
    new_student = {
        "id": new_id,
        "name": data["name"],
        "grade": data["grade"],
        "section": data["section"]
    }
    students.append(new_student)
    return jsonify(new_student), 201

@app.route('/students/<int:student_id>', methods=['PUT'])
def edit_student(student_id):
    data = request.get_json()
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return jsonify({"message": "Student not found"}), 404
    student.update({
        "name": data.get("name", student["name"]),
        "grade": data.get("grade", student["grade"]),
        "section": data.get("section", student["section"])
    })
    return jsonify(student)

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    global students
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return jsonify({"message": "Student not found"}), 404
    students = [s for s in students if s["id"] != student_id]
    return jsonify({"message": "Student deleted"})

if __name__ == '__main__':
    app.run(debug=True)
