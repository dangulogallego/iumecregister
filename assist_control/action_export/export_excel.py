class ExportExcelAction:
    @classmethod

    def generate_header(cls, admin, model, list_display):
        HEADERS_NAMES = {
            'get_date_attended': 'FECHA',
            'get_hour_attended': 'HORA',
            'get_full_name': 'NOMBRES Y APELLIDOS',
            'get_assistan_id': 'CEDULA',
            'temperature': 'TEMPERATURA',
            'get_fever': 'FIEBRE',
            'get_cough': 'TOS',
            'get_headache': 'CEFALEA',
            'get_sore_throat': 'DOLOR DE GARGANTA',
            'get_general_discomfort': 'MALESTAR GENERAL',
            'get_respiratory_difficulty': 'DIFICULTAD RESPIRATORIA',
            'get_adinamia': 'ADINAMIA',
            'get_nasal_secretions': 'SECRECIONES NASALES',
            'get_diarrhea': 'DIARREA',
            'get_close_person': 'CONTACTO CON UN POSITIVO',
            'get_washed': 'DESINFECCIÓN'
        }

        def default_format(value):
            return value.replace('_', ' ').upper()

        header = []
        for field_display in list_display:
            is_model_field = field_display in [f.name for f in model._meta.fields]
            is_admin_field = hasattr(admin, field_display)
            if is_model_field:
                field = model._meta.get_field(field_display)
                # field_name = getattr(field, 'verbose_name', field_display)
                field_name = HEADERS_NAMES[field_display]
                header.append(default_format(field_name))
            elif is_admin_field:
                field = getattr(admin, field_display)
                # field_name = getattr(field, 'short_description', default_format(field_display))
                field_name = HEADERS_NAMES[field_display]
                header.append(default_format(field_name))
            else:
                header.append(default_format(field_display))
        return header
