import React, { useState } from 'react';
import { TextField, Select, MenuItem, FormControl, InputLabel, Button, Box, Grid, Typography, Checkbox, FormControlLabel } from '@mui/material';

interface RecurringTaskFormData {
  title: string;
  description: string;
  dueDate: string;
  reminderEnabled: boolean;
  reminderTime: string;
  recurrencePattern: string;
  recurrenceInterval: number;
  recurrenceEndDate: string;
  timezone: string;
}

interface RecurringTaskFormProps {
  onSubmit: (data: RecurringTaskFormData) => void;
}

const RecurringTaskForm: React.FC<RecurringTaskFormProps> = ({ onSubmit }) => {
  const [formData, setFormData] = useState<RecurringTaskFormData>({
    title: '',
    description: '',
    dueDate: '',
    reminderEnabled: false,
    reminderTime: '',
    recurrencePattern: 'daily',
    recurrenceInterval: 1,
    recurrenceEndDate: '',
    timezone: 'UTC'
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | { name?: string; value: unknown }>) => {
    const { name, value, type } = e.target as HTMLInputElement;
    const checked = type === 'checkbox' ? (e.target as HTMLInputElement).checked : undefined;

    setFormData(prev => ({
      ...prev,
      [name || '']: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
      <Typography variant="h6" gutterBottom>
        Create Recurring Task
      </Typography>

      <Grid container spacing={2}>
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Task Title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            multiline
            rows={3}
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Due Date"
            name="dueDate"
            type="datetime-local"
            value={formData.dueDate}
            onChange={handleChange}
            InputLabelProps={{
              shrink: true,
            }}
          />
        </Grid>

        <Grid item xs={12}>
          <FormControlLabel
            control={
              <Checkbox
                name="reminderEnabled"
                checked={formData.reminderEnabled}
                onChange={(e) => setFormData({...formData, reminderEnabled: e.target.checked})}
              />
            }
            label="Enable Reminder"
          />
        </Grid>

        {formData.reminderEnabled && (
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Reminder Time"
              name="reminderTime"
              type="datetime-local"
              value={formData.reminderTime}
              onChange={handleChange}
              InputLabelProps={{
                shrink: true,
              }}
            />
          </Grid>
        )}

        <Grid item xs={12} sm={6}>
          <FormControl fullWidth required>
            <InputLabel id="recurrence-pattern-label">Recurrence Pattern</InputLabel>
            <Select
              labelId="recurrence-pattern-label"
              name="recurrencePattern"
              value={formData.recurrencePattern}
              label="Recurrence Pattern"
              onChange={(e) => setFormData({...formData, recurrencePattern: e.target.value as string})}
            >
              <MenuItem value="daily">Daily</MenuItem>
              <MenuItem value="weekly">Weekly</MenuItem>
              <MenuItem value="monthly">Monthly</MenuItem>
              <MenuItem value="yearly">Yearly</MenuItem>
              <MenuItem value="custom">Custom</MenuItem>
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            label="Recurrence Interval"
            name="recurrenceInterval"
            type="number"
            value={formData.recurrenceInterval}
            onChange={(e) => setFormData({...formData, recurrenceInterval: parseInt(e.target.value) || 1})}
            inputProps={{ min: 1 }}
            required
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            label="End Date (optional)"
            name="recurrenceEndDate"
            type="date"
            value={formData.recurrenceEndDate}
            onChange={handleChange}
            InputLabelProps={{
              shrink: true,
            }}
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Timezone"
            name="timezone"
            value={formData.timezone}
            onChange={handleChange}
            select
          >
            <MenuItem value="UTC">UTC</MenuItem>
            <MenuItem value="America/New_York">Eastern Time (ET)</MenuItem>
            <MenuItem value="America/Chicago">Central Time (CT)</MenuItem>
            <MenuItem value="America/Denver">Mountain Time (MT)</MenuItem>
            <MenuItem value="America/Los_Angeles">Pacific Time (PT)</MenuItem>
            <MenuItem value="Europe/London">GMT/BST</MenuItem>
            <MenuItem value="Europe/Paris">CET/CEST</MenuItem>
            <MenuItem value="Asia/Tokyo">JST</MenuItem>
          </TextField>
        </Grid>

        <Grid item xs={12}>
          <Button type="submit" variant="contained" color="primary">
            Create Recurring Task
          </Button>
        </Grid>
      </Grid>
    </Box>
  );
};

export default RecurringTaskForm;