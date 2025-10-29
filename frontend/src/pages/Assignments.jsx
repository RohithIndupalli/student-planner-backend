import React, { useState, useEffect } from 'react';
import { assignmentsAPI, coursesAPI } from '../services/api';
import toast from 'react-hot-toast';
import { Plus, Edit2, Trash2, ClipboardList, X, CheckCircle, Circle } from 'lucide-react';
import { format } from 'date-fns';

const Assignments = () => {
  const [assignments, setAssignments] = useState([]);
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingAssignment, setEditingAssignment] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    course_id: '',
    due_date: '',
    priority: 'medium',
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [assignmentsRes, coursesRes] = await Promise.all([
        assignmentsAPI.getAll(),
        coursesAPI.getAll(),
      ]);
      setAssignments(assignmentsRes.data);
      setCourses(coursesRes.data);
      setLoading(false);
    } catch (error) {
      toast.error('Failed to load data');
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingAssignment) {
        await assignmentsAPI.update(editingAssignment.id, formData);
        toast.success('Assignment updated successfully');
      } else {
        await assignmentsAPI.create(formData);
        toast.success('Assignment created successfully! Email notification sent.');
      }
      fetchData();
      closeModal();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to save assignment');
    }
  };

  const handleToggleComplete = async (id) => {
    try {
      await assignmentsAPI.toggleComplete(id);
      toast.success('Assignment status updated');
      fetchData();
    } catch (error) {
      toast.error('Failed to update assignment');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this assignment?')) {
      try {
        await assignmentsAPI.delete(id);
        toast.success('Assignment deleted successfully');
        fetchData();
      } catch (error) {
        toast.error('Failed to delete assignment');
      }
    }
  };

  const openModal = (assignment = null) => {
    if (assignment) {
      setEditingAssignment(assignment);
      setFormData({
        title: assignment.title,
        description: assignment.description || '',
        course_id: assignment.course_id,
        due_date: format(new Date(assignment.due_date), "yyyy-MM-dd'T'HH:mm"),
        priority: assignment.priority,
      });
    } else {
      setEditingAssignment(null);
      setFormData({
        title: '',
        description: '',
        course_id: courses[0]?.id || '',
        due_date: '',
        priority: 'medium',
      });
    }
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setEditingAssignment(null);
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'low':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Assignments</h1>
        <button
          onClick={() => openModal()}
          className="btn-primary flex items-center gap-2"
          disabled={courses.length === 0}
        >
          <Plus className="w-5 h-5" />
          Add Assignment
        </button>
      </div>

      {courses.length === 0 ? (
        <div className="card text-center py-12">
          <ClipboardList className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No courses available</h3>
          <p className="text-gray-600">Please add a course first before creating assignments</p>
        </div>
      ) : assignments.length === 0 ? (
        <div className="card text-center py-12">
          <ClipboardList className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No assignments yet</h3>
          <p className="text-gray-600 mb-4">Get started by adding your first assignment</p>
          <button onClick={() => openModal()} className="btn-primary">
            Add Your First Assignment
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          {assignments.map((assignment) => (
            <div key={assignment.id} className="card">
              <div className="flex items-start gap-4">
                <button
                  onClick={() => handleToggleComplete(assignment.id)}
                  className="mt-1 flex-shrink-0"
                >
                  {assignment.completed ? (
                    <CheckCircle className="w-6 h-6 text-green-600" />
                  ) : (
                    <Circle className="w-6 h-6 text-gray-400 hover:text-indigo-600" />
                  )}
                </button>

                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <h3
                        className={`text-lg font-bold ${
                          assignment.completed ? 'text-gray-500 line-through' : 'text-gray-900'
                        }`}
                      >
                        {assignment.title}
                      </h3>
                      <p className="text-sm text-gray-600 mt-1">{assignment.course_name}</p>
                      {assignment.description && (
                        <p className="text-sm text-gray-500 mt-2">{assignment.description}</p>
                      )}
                      <div className="flex items-center gap-4 mt-3">
                        <span className="text-sm text-gray-600">
                          Due: {format(new Date(assignment.due_date), 'MMM d, yyyy h:mm a')}
                        </span>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(assignment.priority)}`}>
                          {assignment.priority.charAt(0).toUpperCase() + assignment.priority.slice(1)} Priority
                        </span>
                      </div>
                    </div>

                    <div className="flex gap-2 flex-shrink-0">
                      <button
                        onClick={() => openModal(assignment)}
                        className="text-gray-600 hover:text-indigo-600"
                      >
                        <Edit2 className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDelete(assignment.id)}
                        className="text-gray-600 hover:text-red-600"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-md w-full p-6 max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-gray-900">
                {editingAssignment ? 'Edit Assignment' : 'Add New Assignment'}
              </h2>
              <button onClick={closeModal} className="text-gray-500 hover:text-gray-700">
                <X className="w-6 h-6" />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Assignment Title *
                </label>
                <input
                  type="text"
                  required
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="input-field"
                  placeholder="e.g., Chapter 5 Homework"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Course *</label>
                <select
                  required
                  value={formData.course_id}
                  onChange={(e) => setFormData({ ...formData, course_id: e.target.value })}
                  className="input-field"
                >
                  <option value="">Select a course</option>
                  {courses.map((course) => (
                    <option key={course.id} value={course.id}>
                      {course.course_name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Due Date *
                </label>
                <input
                  type="datetime-local"
                  required
                  value={formData.due_date}
                  onChange={(e) => setFormData({ ...formData, due_date: e.target.value })}
                  className="input-field"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Priority</label>
                <select
                  value={formData.priority}
                  onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                  className="input-field"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Description
                </label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="input-field"
                  rows="3"
                  placeholder="Assignment details..."
                />
              </div>

              <div className="flex gap-3 pt-4">
                <button type="submit" className="btn-primary flex-1">
                  {editingAssignment ? 'Update Assignment' : 'Add Assignment'}
                </button>
                <button type="button" onClick={closeModal} className="btn-secondary flex-1">
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Assignments;
