def GetAllRecords(model, serializer):
    records = model.objects.all()
    records = serializer(records, many = True).data
    return records

def GetRecordsFiltered(model, serializer, field, userID):
    if(not field["name"]):
        try:
            data = model.objects.filter(User = userID)
            data = serializer(data, many = True).data
            return data        
        except model.DoesNotExist:
            raise model.DoesNotExist

        
    if field["name"] == 'ID':
        try:
            data = model.objects.get(pk=field['value'])
            data = serializer(data).data
        except model.DoesNotExist:
            raise model.DoesNotExist
        
    else:
        try:
            match field['name']:
                case _:
                    raise model.DoesNotExist
        except model.DoesNotExist:
            raise model.DoesNotExist
    
    return data        
