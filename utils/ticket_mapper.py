# utils/ticket_mapper.py
def map_ticket_type(type_val, title):
    if type_val == 'Platinum' or type_val == 'Delegate Speaker':
        return 'Delegate Pass', '#1428DF'
    if type_val == 'Gold':
        if 'Working' in title:
            return 'Working Pass', '#DAA520'
        return 'Exhibitor Pass', '#FFD700'
    if type_val == 'Silver':
        if 'Investor' in title:
            return 'Investor Pass', '#1E90FF'
        elif 'Mining' in title:
            return 'Mining Pass', '#228B22'
        elif 'Media' in title:
            return 'Media Pass', '#8A2BE2'
        return 'Working Pass', '#DAA520'
    if type_val == 'Speaker':
        return 'Speaker Pass', '#D60000'
    return 'Unknown', '#808080'