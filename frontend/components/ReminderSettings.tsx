import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, TextField, Select, MenuItem, FormControl, InputLabel, Button, Box, Grid, Typography, Switch, FormControlLabel, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

interface ReminderSetting {
  id: string;
  taskId: number;
  taskTitle: string;
  reminderTime: string;
  enabled: boolean;
  method: string;
  lastSent?: string;
}

interface ReminderSettingsProps {
  userId: number;
}

const ReminderSettings: React.FC<ReminderSettingsProps> = ({ userId }) => {
  const [reminders, setReminders] = useState<ReminderSetting[]>([
    // Sample data - in a real app, this would come from an API
    {
      id: '1',
      taskId: 1,
      taskTitle: 'Morning Routine',
      reminderTime: '09:00',
      enabled: true,
      method: 'email'
    },
    {
      id: '2',
      taskId: 2,
      taskTitle: 'Weekly Team Meeting',
      reminderTime: '10:30',
      enabled: true,
      method: 'push'
    },
    {
      id: '3',
      taskId: 3,
      taskTitle: 'Gym Session',
      reminderTime: '18:00',
      enabled: false,
      method: 'sms'
    }
  ]);

  const [newReminder, setNewReminder] = useState({
    taskId: '',
    reminderTime: '',
    method: 'push'
  });

  const handleToggleReminder = (id: string) => {
    setReminders(reminders.map(reminder =>
      reminder.id === id ? { ...reminder, enabled: !reminder.enabled } : reminder
    ));
  };

  const handleAddReminder = () => {
    if (!newReminder.taskId || !newReminder.reminderTime) return;

    const newReminderObj: ReminderSetting = {
      id: Date.now().toString(),
      taskId: parseInt(newReminder.taskId),
      taskTitle: `Task ${newReminder.taskId}`, // In a real app, this would come from the task details
      reminderTime: newReminder.reminderTime,
      enabled: true,
      method: newReminder.method
    };

    setReminders([...reminders, newReminderObj]);
    setNewReminder({ taskId: '', reminderTime: '', method: 'push' });
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setNewReminder({ ...newReminder, [name]: value });
  };

  return (
    <Box sx={{ mt: 2 }}>
      <Card>
        <CardHeader
          title="Reminder Settings"
          subheader="Manage your task reminders and notification preferences"
        />
        <CardContent>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>
                Add New Reminder
              </Typography>

              <Grid container spacing={2}>
                <Grid item xs={12} sm={4}>
                  <TextField
                    fullWidth
                    label="Task ID"
                    name="taskId"
                    value={newReminder.taskId}
                    onChange={handleInputChange}
                    type="number"
                    placeholder="Enter task ID"
                  />
                </Grid>

                <Grid item xs={12} sm={4}>
                  <TextField
                    fullWidth
                    label="Reminder Time"
                    name="reminderTime"
                    type="time"
                    value={newReminder.reminderTime}
                    onChange={handleInputChange}
                    InputLabelProps={{
                      shrink: true,
                    }}
                    inputProps={{
                      step: 300, // 5 min
                    }}
                  />
                </Grid>

                <Grid item xs={12} sm={3}>
                  <FormControl fullWidth>
                    <InputLabel id="notification-method-label">Method</InputLabel>
                    <Select
                      labelId="notification-method-label"
                      name="method"
                      value={newReminder.method}
                      label="Method"
                      onChange={(e) => setNewReminder({...newReminder, method: e.target.value as string})}
                    >
                      <MenuItem value="push">Push Notification</MenuItem>
                      <MenuItem value="email">Email</MenuItem>
                      <MenuItem value="sms">SMS</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>

                <Grid item xs={12} sm={1}>
                  <Button
                    variant="contained"
                    onClick={handleAddReminder}
                    disabled={!newReminder.taskId || !newReminder.reminderTime}
                  >
                    Add
                  </Button>
                </Grid>
              </Grid>
            </Grid>

            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>
                Existing Reminders
              </Typography>

              <TableContainer component={Paper}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Task</TableCell>
                      <TableCell>Reminder Time</TableCell>
                      <TableCell>Method</TableCell>
                      <TableCell>Status</TableCell>
                      <TableCell align="right">Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {reminders.map((reminder) => (
                      <TableRow key={reminder.id}>
                        <TableCell>{reminder.taskTitle}</TableCell>
                        <TableCell>{reminder.reminderTime}</TableCell>
                        <TableCell>
                          {reminder.method === 'push' && 'Push Notification'}
                          {reminder.method === 'email' && 'Email'}
                          {reminder.method === 'sms' && 'SMS'}
                        </TableCell>
                        <TableCell>
                          <Switch
                            checked={reminder.enabled}
                            onChange={() => handleToggleReminder(reminder.id)}
                            inputProps={{ 'aria-label': 'toggle reminder' }}
                          />
                        </TableCell>
                        <TableCell align="right">
                          <Button
                            variant="outlined"
                            size="small"
                            onClick={() => {
                              // Implementation for editing reminder
                            }}
                          >
                            Edit
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Grid>

            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>
                Notification Preferences
              </Typography>

              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <FormControlLabel
                    control={<Switch defaultChecked />}
                    label="Allow desktop notifications"
                  />
                </Grid>

                <Grid item xs={12}>
                  <FormControlLabel
                    control={<Switch defaultChecked />}
                    label="Send email reminders"
                  />
                </Grid>

                <Grid item xs={12}>
                  <FormControlLabel
                    control={<Switch />}
                    label="Send SMS reminders"
                  />
                </Grid>
              </Grid>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    </Box>
  );
};

export default ReminderSettings;