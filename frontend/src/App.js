import React, { useState, useEffect } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStudents();
  }, []);

  const fetchStudents = async () => {
    try {
      const response = await axios.get("http://localhost:5000/api/students");
      setStudents(response.data);
    } catch (error) {
      console.error("Error fetching student data:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-5">
      <h2 className="text-center text-primary mb-4">CBC Blockchain - Student Records</h2>

      {loading ? (
        <p className="text-center text-secondary">Loading student records...</p>
      ) : (
        <table className="table table-striped">
          <thead className="table-dark">
            <tr>
              <th>NEMIS No</th>
              <th>Name</th>
              <th>Institution</th>
              <th>Competency</th>
              <th>Grade</th>
            </tr>
          </thead>
          <tbody>
            {students.length > 0 ? (
              students.map((student) => (
                <tr key={student.id}>
                  <td>{student.nemis_no}</td>
                  <td>{student.name}</td>
                  <td>{student.institution}</td>
                  <td>{student.competency}</td>
                  <td>{student.grade}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="5" className="text-center text-danger">No students found.</td>
              </tr>
            )}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default App;
