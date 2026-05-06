import { useEffect, useState } from "react";
import API from "../services/api";

export default function ListPage() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/api/compliance/all")
      .then(res => setData(res.data))
      .catch(err => console.log(err));
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h2>Compliance Score Leaderboard</h2>

      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>ID</th>
            <th>Employee</th>
            <th>Score</th>
            <th>Department</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {data.map(item => (
            <tr key={item.id}>
              <td>{item.id}</td>
              <td>{item.employeeName}</td>
              <td>{item.score}</td>
              <td>{item.department}</td>
              <td>{item.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}