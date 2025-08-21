'use client';

import { useState, useEffect } from 'react';

interface Task {
  id: string;
  title: string;
  description: string;
  category: string;
  estimated_time: number;
  priority: string;
  completed: boolean;
  completed_date?: string;
  resources: string[];
}

interface OnboardingProgram {
  id: string;
  role: string;
  department: string;
  duration_days: number;
  progress_percentage: number;
  tasks: Task[];
}

interface Employee {
  id: string;
  name: string;
  email: string;
  role: string;
  department: string;
  start_date: string;
  manager: string;
  onboarding_program_id: string;
  status: string;
}

interface EmployeeData {
  employee: Employee;
  program: OnboardingProgram;
}

interface EmployeeSummary {
  employee: Employee;
  progress: number;
  completed_tasks: number;
  total_tasks: number;
}

interface ProgramInfo {
  id: string;
  role: string;
  department: string;
  duration_days: number;
  total_tasks: number;
  task_categories: string[];
  estimated_hours: number;
}

export default function OnboardingPage() {
  const [employees, setEmployees] = useState<EmployeeSummary[]>([]);
  const [selectedEmployee, setSelectedEmployee] = useState<EmployeeData | null>(null);
  const [analytics, setAnalytics] = useState<any>(null);
  const [programs, setPrograms] = useState<Record<string, ProgramInfo>>({});
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [activeTab, setActiveTab] = useState<'dashboard' | 'employees' | 'programs' | 'analytics'>('dashboard');
  const [searchTerm, setSearchTerm] = useState('');
  const [filterRole, setFilterRole] = useState('');
  const [newEmployee, setNewEmployee] = useState({
    name: '',
    email: '',
    role: 'Teller',
    department: 'Branch Operations',
    manager: ''
  });

  const roles = [
    { value: 'Teller', department: 'Branch Operations' },
    { value: 'Personal Banker', department: 'Retail Banking' },
    { value: 'Business Banking Specialist', department: 'Commercial Banking' },
    { value: 'Loan Officer', department: 'Lending' },
    { value: 'Investment Advisor', department: 'Wealth Management' }
  ];

  useEffect(() => {
    loadEmployees();
    loadAnalytics();
    loadPrograms();
  }, []);

  const loadEmployees = async () => {
    try {
      const response = await fetch('/api/onboarding/employees');
      const data = await response.json();
      setEmployees(data.employees || []);
    } catch (error) {
      console.error('Failed to load employees:', error);
    }
  };

  const loadAnalytics = async () => {
    try {
      const response = await fetch('/api/onboarding/analytics');
      const data = await response.json();
      setAnalytics(data);
    } catch (error) {
      console.error('Failed to load analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadPrograms = async () => {
    try {
      const response = await fetch('/api/onboarding/programs');
      const data = await response.json();
      setPrograms(data.programs || {});
    } catch (error) {
      console.error('Failed to load programs:', error);
    }
  };

  const loadEmployeeDetails = async (employeeId: string) => {
    try {
      const response = await fetch(`/api/onboarding/employees/${employeeId}`);
      const data = await response.json();
      setSelectedEmployee(data);
    } catch (error) {
      console.error('Failed to load employee details:', error);
    }
  };

  const completeTask = async (employeeId: string, taskId: string) => {
    try {
      const response = await fetch(`/api/onboarding/employees/${employeeId}/complete-task`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ task_id: taskId }),
      });
      
      if (response.ok) {
        // Reload employee details and analytics
        await loadEmployeeDetails(employeeId);
        await loadEmployees();
        await loadAnalytics();
      }
    } catch (error) {
      console.error('Failed to complete task:', error);
    }
  };

  const createEmployee = async () => {
    try {
      const response = await fetch('/api/onboarding/employees', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newEmployee),
      });
      
      if (response.ok) {
        setShowCreateForm(false);
        setNewEmployee({
          name: '',
          email: '',
          role: 'Teller',
          department: 'Branch Operations',
          manager: ''
        });
        await loadEmployees();
        await loadAnalytics();
      }
    } catch (error) {
      console.error('Failed to create employee:', error);
    }
  };

  const createDemoData = async () => {
    try {
      const response = await fetch('/api/onboarding/demo-data', {
        method: 'POST',
      });
      
      if (response.ok) {
        await loadEmployees();
        await loadAnalytics();
        setActiveTab('employees');
      }
    } catch (error) {
      console.error('Failed to create demo data:', error);
    }
  };

  const clearAllData = async () => {
    try {
      const response = await fetch('/api/onboarding/clear', {
        method: 'POST',
      });
      
      if (response.ok) {
        await loadEmployees();
        await loadAnalytics();
        setSelectedEmployee(null);
      }
    } catch (error) {
      console.error('Failed to clear data:', error);
    }
  };

  // Filter employees based on search and role
  const filteredEmployees = employees.filter(emp => {
    const matchesSearch = emp.employee.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         emp.employee.email.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesRole = !filterRole || emp.employee.role === filterRole;
    return matchesSearch && matchesRole;
  });

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'text-red-600 bg-red-50';
      case 'medium': return 'text-yellow-600 bg-yellow-50';
      case 'low': return 'text-green-600 bg-green-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  const getProgressColor = (progress: number) => {
    if (progress >= 80) return 'bg-green-500';
    if (progress >= 50) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Employee Onboarding</h1>
              <p className="text-gray-600 text-sm">AI-powered HR workflow management</p>
            </div>
            <div className="flex items-center space-x-3">
              <button
                onClick={createDemoData}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
              >
                Generate Demo Data
              </button>
              <button
                onClick={() => setShowCreateForm(true)}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm font-medium"
              >
                + Add Employee
              </button>
              <button
                onClick={clearAllData}
                className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors text-sm font-medium"
              >
                Clear All
              </button>
            </div>
          </div>
          
          {/* Tab Navigation */}
          <div className="mt-4 border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              {[
                { id: 'dashboard', label: 'Dashboard', icon: '📊' },
                { id: 'employees', label: 'Employees', icon: '👥' },
                { id: 'programs', label: 'Programs', icon: '📋' },
                { id: 'analytics', label: 'Analytics', icon: '📈' }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`py-2 px-1 border-b-2 font-medium text-sm whitespace-nowrap ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <span className="mr-2">{tab.icon}</span>
                  {tab.label}
                </button>
              ))}
            </nav>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-6">
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <>
            {/* Dashboard Tab */}
            {activeTab === 'dashboard' && (
              <div className="space-y-6">
                {/* Quick Stats */}
                {analytics && (
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                      <div className="flex items-center">
                        <div className="text-3xl text-blue-600 mr-4">👥</div>
                        <div>
                          <h3 className="text-lg font-semibold text-gray-900">Total Employees</h3>
                          <p className="text-2xl font-bold text-blue-600">{analytics.total_employees}</p>
                        </div>
                      </div>
                    </div>
                    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                      <div className="flex items-center">
                        <div className="text-3xl text-green-600 mr-4">📈</div>
                        <div>
                          <h3 className="text-lg font-semibold text-gray-900">Avg Progress</h3>
                          <p className="text-2xl font-bold text-green-600">{analytics.average_progress.toFixed(1)}%</p>
                        </div>
                      </div>
                    </div>
                    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                      <div className="flex items-center">
                        <div className="text-3xl text-purple-600 mr-4">✅</div>
                        <div>
                          <h3 className="text-lg font-semibold text-gray-900">Completion Rate</h3>
                          <p className="text-2xl font-bold text-purple-600">{(analytics.completion_rate * 100).toFixed(1)}%</p>
                        </div>
                      </div>
                    </div>
                    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                      <div className="flex items-center">
                        <div className="text-3xl text-orange-600 mr-4">📋</div>
                        <div>
                          <h3 className="text-lg font-semibold text-gray-900">Active Programs</h3>
                          <p className="text-2xl font-bold text-orange-600">{Object.keys(analytics.by_role || {}).length}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {/* Role Breakdown */}
                {analytics?.by_role && (
                  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Progress by Role</h3>
                    <div className="space-y-4">
                      {Object.entries(analytics.by_role).map(([role, data]: [string, any]) => (
                        <div key={role} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                          <div>
                            <h4 className="font-medium text-gray-900">{role}</h4>
                            <p className="text-sm text-gray-600">{data.count} employees</p>
                          </div>
                          <div className="flex items-center space-x-4">
                            <div className="text-right">
                              <div className="text-lg font-bold text-gray-900">{data.average_progress.toFixed(1)}%</div>
                              <div className="w-32 bg-gray-200 rounded-full h-2">
                                <div
                                  className={`h-2 rounded-full ${getProgressColor(data.average_progress)}`}
                                  style={{ width: `${data.average_progress}%` }}
                                ></div>
                              </div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Recent Activity */}
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <button
                      onClick={() => setActiveTab('employees')}
                      className="p-4 text-left border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                    >
                      <div className="text-2xl text-blue-600 mb-2">👥</div>
                      <h4 className="font-medium text-gray-900">Manage Employees</h4>
                      <p className="text-sm text-gray-600">View and manage employee onboarding progress</p>
                    </button>
                    <button
                      onClick={() => setActiveTab('programs')}
                      className="p-4 text-left border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                    >
                      <div className="text-2xl text-orange-600 mb-2">📋</div>
                      <h4 className="font-medium text-gray-900">View Programs</h4>
                      <p className="text-sm text-gray-600">Explore onboarding programs and curricula</p>
                    </button>
                    <button
                      onClick={() => setActiveTab('analytics')}
                      className="p-4 text-left border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                    >
                      <div className="text-2xl text-green-600 mb-2">📈</div>
                      <h4 className="font-medium text-gray-900">View Analytics</h4>
                      <p className="text-sm text-gray-600">Detailed insights and performance metrics</p>
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Employees Tab */}
            {activeTab === 'employees' && (
              <div className="space-y-6">
                {/* Search and Filter Controls */}
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
                  <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-3 md:space-y-0">
                    <div className="flex flex-col md:flex-row md:items-center space-y-3 md:space-y-0 md:space-x-4">
                      <div className="relative">
                        <input
                          type="text"
                          placeholder="Search employees..."
                          value={searchTerm}
                          onChange={(e) => setSearchTerm(e.target.value)}
                          className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 w-full md:w-64"
                        />
                        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                          <svg className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                          </svg>
                        </div>
                      </div>
                      <select
                        value={filterRole}
                        onChange={(e) => setFilterRole(e.target.value)}
                        className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="">All Roles</option>
                        <option value="Teller">Teller</option>
                        <option value="Personal Banker">Personal Banker</option>
                        <option value="Business Banking Specialist">Business Banking Specialist</option>
                      </select>
                    </div>
                    <div className="text-sm text-gray-600">
                      Showing {filteredEmployees.length} of {employees.length} employees
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Employee List */}
                  <div className="bg-white rounded-lg shadow-sm border border-gray-200">
                    <div className="p-6 border-b border-gray-200">
                      <h2 className="text-xl font-semibold text-gray-900">Employees</h2>
                    </div>
                    <div className="p-6">
                      {filteredEmployees.length === 0 ? (
                        <div className="text-center py-8">
                          <div className="text-gray-400 mb-4">
                            <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                            </svg>
                          </div>
                          <p className="text-gray-500 mb-4">No employees found</p>
                          <button
                            onClick={createDemoData}
                            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                          >
                            Generate Demo Data
                          </button>
                        </div>
                      ) : (
                        <div className="space-y-3 max-h-96 overflow-y-auto">
                          {filteredEmployees.map((emp) => (
                            <div
                              key={emp.employee.id}
                              className={`border rounded-lg p-4 cursor-pointer transition-all duration-200 ${
                                selectedEmployee?.employee.id === emp.employee.id
                                  ? 'border-blue-500 bg-blue-50'
                                  : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                              }`}
                              onClick={() => loadEmployeeDetails(emp.employee.id)}
                            >
                              <div className="flex justify-between items-start mb-3">
                                <div>
                                  <h3 className="font-semibold text-gray-900">{emp.employee.name}</h3>
                                  <p className="text-sm text-gray-600">{emp.employee.role}</p>
                                  <p className="text-xs text-gray-500">{emp.employee.department}</p>
                                </div>
                                <div className="text-right">
                                  <span className={`text-lg font-bold ${getProgressColor(emp.progress) === 'bg-green-500' ? 'text-green-600' : getProgressColor(emp.progress) === 'bg-yellow-500' ? 'text-yellow-600' : 'text-red-600'}`}>
                                    {emp.progress.toFixed(0)}%
                                  </span>
                                  <p className="text-xs text-gray-500">{emp.completed_tasks}/{emp.total_tasks} tasks</p>
                                </div>
                              </div>
                              <div className="w-full bg-gray-200 rounded-full h-2">
                                <div
                                  className={`h-2 rounded-full transition-all duration-300 ${getProgressColor(emp.progress)}`}
                                  style={{ width: `${emp.progress}%` }}
                                ></div>
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Employee Details Panel */}
                  <div className="bg-white rounded-lg shadow-sm border border-gray-200">
                    <div className="p-6 border-b border-gray-200">
                      <h2 className="text-xl font-semibold text-gray-900">
                        {selectedEmployee ? 'Employee Details' : 'Select an Employee'}
                      </h2>
                    </div>
                    <div className="p-6">
                      {selectedEmployee ? (
                        <div className="space-y-6">
                          {/* Employee Info Card */}
                          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-4 border border-blue-200">
                            <div className="flex justify-between items-start mb-4">
                              <div>
                                <h3 className="text-xl font-bold text-gray-900">{selectedEmployee.employee.name}</h3>
                                <p className="text-blue-700 font-medium">{selectedEmployee.employee.role}</p>
                                <p className="text-gray-600">{selectedEmployee.employee.department}</p>
                              </div>
                              <div className="text-right">
                                <div className="text-2xl font-bold text-blue-600">
                                  {selectedEmployee.program.progress_percentage.toFixed(0)}%
                                </div>
                                <p className="text-sm text-gray-600">Complete</p>
                              </div>
                            </div>
                            <div className="grid grid-cols-2 gap-4 text-sm">
                              <div><span className="text-gray-500">Manager:</span> {selectedEmployee.employee.manager}</div>
                              <div><span className="text-gray-500">Start Date:</span> {selectedEmployee.employee.start_date}</div>
                              <div><span className="text-gray-500">Email:</span> {selectedEmployee.employee.email}</div>
                              <div><span className="text-gray-500">Status:</span> 
                                <span className="ml-1 px-2 py-1 rounded-full text-xs bg-green-100 text-green-800">
                                  {selectedEmployee.employee.status}
                                </span>
                              </div>
                            </div>
                            <div className="mt-4">
                              <div className="w-full bg-blue-200 rounded-full h-3">
                                <div
                                  className="h-3 rounded-full bg-blue-600 transition-all duration-500"
                                  style={{ width: `${selectedEmployee.program.progress_percentage}%` }}
                                ></div>
                              </div>
                            </div>
                          </div>

                          {/* Task Management */}
                          <div>
                            <div className="flex justify-between items-center mb-4">
                              <h4 className="text-lg font-semibold text-gray-900">Onboarding Tasks</h4>
                              <div className="text-sm text-gray-600">
                                {selectedEmployee.program.tasks.filter(t => t.completed).length} of {selectedEmployee.program.tasks.length} completed
                              </div>
                            </div>
                            <div className="space-y-3 max-h-80 overflow-y-auto">
                              {selectedEmployee.program.tasks.map((task) => (
                                <div
                                  key={task.id}
                                  className={`border rounded-lg p-4 transition-all duration-200 ${
                                    task.completed 
                                      ? 'bg-green-50 border-green-200' 
                                      : 'bg-white border-gray-200 hover:border-blue-300 hover:shadow-sm'
                                  }`}
                                >
                                  <div className="flex justify-between items-start">
                                    <div className="flex-1">
                                      <div className="flex items-center space-x-3 mb-2">
                                        <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${
                                          task.completed ? 'bg-green-500 border-green-500' : 'border-gray-300'
                                        }`}>
                                          {task.completed && (
                                            <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                                              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                            </svg>
                                          )}
                                        </div>
                                        <h5 className={`font-medium ${task.completed ? 'text-green-800' : 'text-gray-900'}`}>
                                          {task.title}
                                        </h5>
                                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(task.priority)}`}>
                                          {task.priority}
                                        </span>
                                      </div>
                                      <p className={`text-sm ${task.completed ? 'text-green-700' : 'text-gray-600'} mb-2 ml-8`}>
                                        {task.description}
                                      </p>
                                      <div className="flex items-center space-x-4 text-xs text-gray-500 ml-8">
                                        <span>📂 {task.category}</span>
                                        <span>⏱️ {task.estimated_time} min</span>
                                      </div>
                                      {task.resources.length > 0 && (
                                        <div className="mt-2 ml-8">
                                          <span className="text-xs text-gray-500">📚 Resources: </span>
                                          <span className="text-xs text-blue-600">{task.resources.join(', ')}</span>
                                        </div>
                                      )}
                                      {task.completed && task.completed_date && (
                                        <div className="mt-2 ml-8 text-xs text-green-600 font-medium">
                                          ✅ Completed on {new Date(task.completed_date).toLocaleDateString()}
                                        </div>
                                      )}
                                    </div>
                                    {!task.completed && (
                                      <button
                                        onClick={() => completeTask(selectedEmployee.employee.id, task.id)}
                                        className="ml-4 px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 transition-colors font-medium"
                                      >
                                        Complete Task
                                      </button>
                                    )}
                                  </div>
                                </div>
                              ))}
                            </div>
                          </div>
                        </div>
                      ) : (
                        <div className="text-center py-12">
                          <div className="text-gray-400 mb-4">
                            <svg className="mx-auto h-16 w-16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                            </svg>
                          </div>
                          <h3 className="text-lg font-medium text-gray-900 mb-2">No Employee Selected</h3>
                          <p className="text-gray-500">Click on an employee from the list to view their onboarding progress and tasks</p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Programs Tab */}
            {activeTab === 'programs' && (
              <div className="space-y-6">
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <h2 className="text-xl font-semibold text-gray-900 mb-6">Onboarding Programs</h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {Object.entries(programs).map(([key, program]) => (
                      <div key={key} className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                        <div className="flex items-center justify-between mb-4">
                          <h3 className="text-lg font-semibold text-gray-900">{program.role}</h3>
                          <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                            {program.duration_days} days
                          </span>
                        </div>
                        <p className="text-gray-600 mb-4">{program.department}</p>
                        
                        <div className="space-y-3">
                          <div className="flex justify-between text-sm">
                            <span className="text-gray-500">Total Tasks:</span>
                            <span className="font-medium">{program.total_tasks}</span>
                          </div>
                          <div className="flex justify-between text-sm">
                            <span className="text-gray-500">Estimated Hours:</span>
                            <span className="font-medium">{program.estimated_hours.toFixed(1)}h</span>
                          </div>
                          <div className="pt-3 border-t border-gray-200">
                            <p className="text-sm text-gray-500 mb-2">Task Categories:</p>
                            <div className="flex flex-wrap gap-1">
                              {program.task_categories.map((category, index) => (
                                <span key={index} className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs">
                                  {category}
                                </span>
                              ))}
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Analytics Tab */}
            {activeTab === 'analytics' && analytics && (
              <div className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Role Performance */}
                  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance by Role</h3>
                    <div className="space-y-4">
                      {Object.entries(analytics.by_role || {}).map(([role, data]: [string, any]) => (
                        <div key={role} className="p-4 bg-gray-50 rounded-lg">
                          <div className="flex justify-between items-center mb-2">
                            <h4 className="font-medium text-gray-900">{role}</h4>
                            <span className="text-lg font-bold text-blue-600">{data.average_progress.toFixed(1)}%</span>
                          </div>
                          <div className="grid grid-cols-3 gap-4 text-sm text-gray-600">
                            <div>
                              <span className="block text-xs text-gray-500">Employees</span>
                              <span className="font-medium text-gray-900">{data.count}</span>
                            </div>
                            <div>
                              <span className="block text-xs text-gray-500">Completed</span>
                              <span className="font-medium text-gray-900">{data.completed}</span>
                            </div>
                            <div>
                              <span className="block text-xs text-gray-500">Rate</span>
                              <span className="font-medium text-gray-900">{(data.completion_rate * 100).toFixed(1)}%</span>
                            </div>
                          </div>
                          <div className="mt-3">
                            <div className="w-full bg-gray-200 rounded-full h-2">
                              <div
                                className={`h-2 rounded-full ${getProgressColor(data.average_progress)}`}
                                style={{ width: `${data.average_progress}%` }}
                              ></div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Quick Insights */}
                  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Key Insights</h3>
                    <div className="space-y-4">
                      <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                        <h4 className="font-medium text-blue-900 mb-1">Total Progress</h4>
                        <p className="text-2xl font-bold text-blue-600">{analytics.average_progress.toFixed(1)}%</p>
                        <p className="text-sm text-blue-700">Average across all employees</p>
                      </div>
                      
                      <div className="p-4 bg-green-50 rounded-lg border border-green-200">
                        <h4 className="font-medium text-green-900 mb-1">Active Onboarding</h4>
                        <p className="text-2xl font-bold text-green-600">{analytics.total_employees}</p>
                        <p className="text-sm text-green-700">Employees currently onboarding</p>
                      </div>
                      
                      <div className="p-4 bg-purple-50 rounded-lg border border-purple-200">
                        <h4 className="font-medium text-purple-900 mb-1">Completion Rate</h4>
                        <p className="text-2xl font-bold text-purple-600">{(analytics.completion_rate * 100).toFixed(1)}%</p>
                        <p className="text-sm text-purple-700">Successfully completed programs</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </>
        )}
      </div>

      {/* Create Employee Modal */}
      {showCreateForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md mx-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Add New Employee</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                <input
                  type="text"
                  value={newEmployee.name}
                  onChange={(e) => setNewEmployee({...newEmployee, name: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter employee name"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input
                  type="email"
                  value={newEmployee.email}
                  onChange={(e) => setNewEmployee({...newEmployee, email: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter email address"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Role</label>
                <select
                  value={newEmployee.role}
                  onChange={(e) => {
                    const selectedRole = roles.find(r => r.value === e.target.value);
                    setNewEmployee({
                      ...newEmployee, 
                      role: e.target.value,
                      department: selectedRole?.department || ''
                    });
                  }}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  {roles.map(role => (
                    <option key={role.value} value={role.value}>{role.value}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Manager</label>
                <input
                  type="text"
                  value={newEmployee.manager}
                  onChange={(e) => setNewEmployee({...newEmployee, manager: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter manager name"
                />
              </div>
            </div>
            <div className="flex justify-end space-x-3 mt-6">
              <button
                onClick={() => setShowCreateForm(false)}
                className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={createEmployee}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Create Employee
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
