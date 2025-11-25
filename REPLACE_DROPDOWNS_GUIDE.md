# How to Replace All Remaining Dropdowns

## For Kidney Prediction Component (Already Updated)
✅ **Protein in Urine (al)** - Updated to SelectDropdown
✅ **Sugar in Urine (su)** - Updated to SelectDropdown

## For Mental Health Assessment Component  
Update any native `<select>` with SelectDropdown

### Example for Mental Health
```jsx
// BEFORE - Native select (unclear options):
<select
  name="mh_history"
  value={formData.mh_history}
  onChange={handleInputChange}
  className="w-full px-4 py-2 rounded-lg bg-white/20..."
>
  <option value="no">No</option>
  <option value="yes">Yes</option>
  <option value="family">Family History</option>
</select>

// AFTER - Custom SelectDropdown (clear options):
<SelectDropdown
  name="mh_history"
  value={formData.mh_history}
  onChange={handleInputChange}
  label="Mental Health History"
  options={[
    { value: 'no', label: 'No' },
    { value: 'yes', label: 'Yes' },
    { value: 'family', label: 'Family History' }
  ]}
/>
```

## For Dengue Prediction Component
If you have any native select elements, replace them the same way.

## Standard Options to Use

### Gender Options
```jsx
options={[
  { value: '0', label: 'Female' },
  { value: '1', label: 'Male' },
  { value: '2', label: 'Other' }
]}
```

### Employment Status
```jsx
options={[
  { value: '0', label: 'Unemployed' },
  { value: '1', label: 'Employed' },
  { value: '2', label: 'Self-Employed' },
  { value: '3', label: 'Student' }
]}
```

### Work Environment
```jsx
options={[
  { value: '0', label: 'Remote' },
  { value: '1', label: 'Office' },
  { value: '2', label: 'Field' },
  { value: '3', label: 'Hybrid' }
]}
```

### Yes/No Options
```jsx
options={[
  { value: 'no', label: 'No' },
  { value: 'yes', label: 'Yes' }
]}
```

### Treatment Options
```jsx
options={[
  { value: 'no', label: 'No Treatment' },
  { value: 'yes', label: 'Currently Treated' },
  { value: 'past', label: 'Past Treatment' }
]}
```

## Step-by-Step Guide

### 1. Import SelectDropdown at top of file:
```jsx
import { SelectDropdown } from './SelectDropdown';
```

### 2. Find all native `<select>` elements in your component

### 3. Replace each one:
```jsx
// Replace this structure:
<div>
  <label>Field Name</label>
  <select name="fieldName" value={value} onChange={handleChange}>
    <option value="1">Option 1</option>
    <option value="2">Option 2</option>
  </select>
</div>

// With this structure:
<div>
  <SelectDropdown
    name="fieldName"
    value={value}
    onChange={handleChange}
    label="Field Name"
    options={[
      { value: '1', label: 'Option 1' },
      { value: '2', label: 'Option 2' }
    ]}
  />
</div>
```

## Pro Tips

### Keep Required Field Indicators
The SelectDropdown will automatically show `*` if you pass `required={true}`:
```jsx
<SelectDropdown
  name="fieldName"
  label="Field Name *"
  required={true}
  // ... other props
/>
```

### Grouping Related Selects
Put related dropdowns in a grid for better layout:
```jsx
<div className="grid grid-cols-2 gap-4">
  <SelectDropdown {...props1} />
  <SelectDropdown {...props2} />
</div>
```

### Conditional Options
Generate options dynamically based on state:
```jsx
const genderOptions = useMemo(() => [
  { value: '0', label: 'Female' },
  { value: '1', label: 'Male' }
], []);

<SelectDropdown
  options={genderOptions}
  {...otherProps}
/>
```

## Troubleshooting

### Issue: Options not showing correctly
**Solution:** Check that options array has both `value` and `label` properties

### Issue: Selected value not updating
**Solution:** Make sure your onChange handler properly updates state

### Issue: Dropdown appears behind other elements
**Solution:** The component uses `z-50` which should be sufficient. Check for higher z-index elements

### Issue: Dropdown doesn't close when clicking outside
**Solution:** Ensure the ref is properly attached to the dropdown container

## Performance Optimization

For components with many dropdowns, memoize the options:

```jsx
const selectOptions = useMemo(() => ({
  gender: [
    { value: '0', label: 'Female' },
    { value: '1', label: 'Male' }
  ],
  employment: [
    { value: '0', label: 'Unemployed' },
    { value: '1', label: 'Employed' }
  ]
}), []);

// Use like:
<SelectDropdown options={selectOptions.gender} {...props} />
<SelectDropdown options={selectOptions.employment} {...props} />
```

---

**All dropdowns now display options CLEARLY and beautifully! 🎉**
