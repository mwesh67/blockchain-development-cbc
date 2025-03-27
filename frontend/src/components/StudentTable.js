import React, { useEffect, useState } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";

const StudentTable = () => {
  const [students, setStudents] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:5000/api/students") 
      .then((response) => {
        setStudents(response.data);
      })
      .catch((error) => {
        console.error("Error fetching students:", error);
      });
  }, []);

  return (
    <div className="container mt-5">
      <h2 className="text-center mb-4">Student List</h2>
      <table className="table table-striped">
        <thead className="table-dark">
          <tr>
            <th>NEMIS No</th>
            <th>Name</th>
            <th>Institution</th>
            <th>Competency</th>
            <th>Grade</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {students.length > 0 ? (
            students.map((student, index) => (
              <tr key={index}>
                <td>{student.nemis_no}</td>
                <td>{student.name}</td>
                <td>{student.institution}</td>
                <td>{student.competency}</td>
                <td>{student.grade}</td>
                <td>{student.timestamp}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="6" className="text-center">
                No students found.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default StudentTable;
