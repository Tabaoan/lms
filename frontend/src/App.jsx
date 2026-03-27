import { useState, useEffect } from 'react';

const API_URL = 'http://localhost:4000/api';

export default function App() {
  const [classes, setClasses] = useState([]);
  
  const [parent, setParent] = useState({ name: '', phone: '', email: '' });
  const [student, setStudent] = useState({ name: '', dob: '', gender: 'Nam', current_grade: '', parent_id: '' });
  
  const [regStudentId, setRegStudentId] = useState('');
  const [regClassId, setRegClassId] = useState('');

  const fetchClasses = async () => {
    try {
      const res = await fetch(`${API_URL}/classes`);
      const data = await res.json();
      setClasses(data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchClasses();
  }, []);

  const handleCreateParent = async (e) => {
    e.preventDefault();
    const res = await fetch(`${API_URL}/parents`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(parent)
    });
    const data = await res.json();
    if (res.ok) {
      alert('Tạo Phụ huynh thành công! Đã tự động điền ID sang form Học Sinh.');
      setStudent({...student, parent_id: data.id});
    } else {
      alert('Lỗi: ' + JSON.stringify(data));
    }
  };

  const handleCreateStudent = async (e) => {
    e.preventDefault();
    const formattedData = { ...student, dob: new Date(student.dob).toISOString() };
    const res = await fetch(`${API_URL}/students`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formattedData)
    });
    const data = await res.json();
    if (res.ok) {
      alert('Tạo Học sinh thành công! Đã tự động điền ID sang form Đăng Ký.');
      setRegStudentId(data.id);
    } else {
      alert('Lỗi: ' + JSON.stringify(data));
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    const res = await fetch(`${API_URL}/classes/${regClassId}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ student_id: regStudentId })
    });
    const data = await res.json();
    if (res.ok) {
      alert('Đăng ký lớp thành công!');
      fetchClasses();
    } else {
      alert('Lỗi: ' + data.detail);
    }
  };

  const daysOfWeek = [
    { label: 'Thứ 2', val: 1 }, { label: 'Thứ 3', val: 2 }, { label: 'Thứ 4', val: 3 },
    { label: 'Thứ 5', val: 4 }, { label: 'Thứ 6', val: 5 }, { label: 'Thứ 7', val: 6 },
    { label: 'Chủ Nhật', val: 0 }
  ];

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif', maxWidth: '1200px', margin: '0 auto' }}>
      <h1 style={{ textAlign: 'center', borderBottom: '2px solid #ccc', paddingBottom: '10px' }}>Mini LMS - Product Builder</h1>
      
      <div style={{ display: 'flex', gap: '20px', marginBottom: '30px' }}>
        <div style={{ flex: 1, border: '1px solid #ddd', padding: '15px', borderRadius: '8px' }}>
          <h3>1. Tạo Phụ Huynh</h3>
          <form onSubmit={handleCreateParent} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <input type="text" placeholder="Tên phụ huynh" required onChange={e => setParent({...parent, name: e.target.value})} />
            <input type="text" placeholder="Số điện thoại" required onChange={e => setParent({...parent, phone: e.target.value})} />
            <input type="email" placeholder="Email" required onChange={e => setParent({...parent, email: e.target.value})} />
            <button type="submit" style={{ cursor: 'pointer', padding: '8px', background: '#4CAF50', color: 'white', border: 'none' }}>Tạo Phụ Huynh</button>
          </form>
        </div>

        <div style={{ flex: 1, border: '1px solid #ddd', padding: '15px', borderRadius: '8px' }}>
          <h3>2. Tạo Học Sinh</h3>
          <form onSubmit={handleCreateStudent} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <input type="text" placeholder="Tên học sinh" required onChange={e => setStudent({...student, name: e.target.value})} />
            <input type="date" required onChange={e => setStudent({...student, dob: e.target.value})} />
            <select onChange={e => setStudent({...student, gender: e.target.value})}>
              <option value="Nam">Nam</option>
              <option value="Nữ">Nữ</option>
            </select>
            <input type="text" placeholder="Khối/Lớp (VD: Lớp 10)" required onChange={e => setStudent({...student, current_grade: e.target.value})} />
            <input type="text" placeholder="ID Phụ huynh (Tự động điền)" required value={student.parent_id} onChange={e => setStudent({...student, parent_id: e.target.value})} />
            <button type="submit" style={{ cursor: 'pointer', padding: '8px', background: '#2196F3', color: 'white', border: 'none' }}>Tạo Học Sinh</button>
          </form>
        </div>

        <div style={{ flex: 1, border: '1px solid #ddd', padding: '15px', borderRadius: '8px', background: '#f9f9f9' }}>
          <h3>3. Đăng Ký Lớp Học</h3>
          <form onSubmit={handleRegister} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <input type="text" placeholder="ID Học sinh (Tự động điền)" required value={regStudentId} onChange={e => setRegStudentId(e.target.value)} />
            <select required value={regClassId} onChange={e => setRegClassId(e.target.value)}>
              <option value="">-- Chọn lớp học --</option>
              {classes.map(c => (
                <option key={c.id} value={c.id}>{c.name} ({c.time_slot}) - Sĩ số: {c._count?.registrations}/{c.max_students}</option>
              ))}
            </select>
            <button type="submit" style={{ cursor: 'pointer', padding: '8px', background: '#FF9800', color: 'white', border: 'none' }}>Xác nhận Đăng ký</button>
            <small style={{ color: '#666' }}>Lưu ý: Học sinh cần có gói học (Subscription) tạo qua API trước.</small>
          </form>
        </div>
      </div>

      <h3>Danh sách Lớp học theo tuần</h3>
      <table border="1" style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', tableLayout: 'fixed' }}>
        <thead style={{ background: '#eee' }}>
          <tr>
            {daysOfWeek.map(day => <th key={day.val} style={{ padding: '10px' }}>{day.label}</th>)}
          </tr>
        </thead>
        <tbody>
          <tr>
            {daysOfWeek.map(day => (
              <td key={day.val} style={{ verticalAlign: 'top', padding: '10px', height: '150px' }}>
                {classes.filter(c => c.day_of_week === day.val).map(c => (
                  <div key={c.id} style={{ background: '#e3f2fd', margin: '5px 0', padding: '8px', borderRadius: '4px', fontSize: '14px' }}>
                    <strong>{c.name}</strong><br/>
                    Giờ học: {c.time_slot}<br/>
                    Giáo viên: {c.teacher_name}<br/>
                    Sĩ số: {c._count?.registrations || 0}/{c.max_students}
                  </div>
                ))}
              </td>
            ))}
          </tr>
        </tbody>
      </table>
    </div>
  );
}