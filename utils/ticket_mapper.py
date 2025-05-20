# utils/ticket_mapper.py
def map_ticket_type(type_val, title):
    if type_val == 'Platinum' or type_val == 'Delegate Speaker':
        return 'Delegate Pass'
    if type_val == 'Gold':
        if 'Working' in title:
            return 'Working Pass'
        return 'Exhibitor Pass'
    if type_val == 'Silver':
        if 'Investor' in title:
            return 'Investor Pass'
        elif 'Mining' in title:
            return 'Mining Pass'
        elif 'Media' in title:
            return 'Media Pass'
        return 'Working Pass'
    if type_val == 'Speaker':
        return 'Speaker Pass'
    return 'Unknown'