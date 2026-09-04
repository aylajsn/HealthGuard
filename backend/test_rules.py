from rule_checks import find_phi_fields

sample_data = {
    "patient_name": "Jane Doe",
    "heart_rate": 72,
    "random_field": "hello"
}

findings = find_phi_fields(sample_data)
for f in findings:
    print(f"Field: {f['field']} | Category: {f['category']} | {f['recommendation']}")