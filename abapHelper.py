import DataStructure
from abap.abapFunction import AbapFunction

basic_types = ['Z_REINF_PERIODO', 'Z_REINF_TEXTO', 'Z_REINF_NUMERO', 'Z_REINF_VALOR', 'Z_REINF_DATA']


class AbapHelper:
    def __init__(self):
        pass

    @staticmethod
    def local_table_type(type_name):
        return ['TYPES ' + type_name + '_T TYPE TABLE OF ' + type_name + ' WITH NON-UNIQUE DEFAULT KEY.']

    @staticmethod
    def local_types_begin(type_name, begin=True):
        return ['TYPES: BEGIN OF ' + type_name + ',']

    @staticmethod
    def local_types_end(type_name):
        return ['END OF ' + type_name + '.\n']

    @staticmethod
    def local_types_line(var_name, type_name):
        return [str(var_name) + ' type ' + str(type_name) + ',']

    @staticmethod
    def cat_tab_info(tab_cat_name, struct_name, descricao):
        command = list()
        command.append('wa_dd40v-typename = \'Y' + tab_cat_name + '\'.')
        command.append('wa_dd40v-rowtype = \'Y' + struct_name + '\'.')
        command.append('wa_dd40v-ddlanguage = sy-langu.')
        command.append('wa_dd40v-rowkind = \'S\'.')
        command.append('wa_dd40v-accessmode = \'T\'.')
        command.append('wa_dd40v-keydef = \'D\'.')
        command.append('wa_dd40v-ddtext = \'' + descricao + '\'.')
        command.append('wa_dd40v-as4user = sy-uname.')
        command.append('wa_dd40v-as4date = sy-datum.')
        command.append('wa_dd40v-as4time = sy-uzeit.')
        return command

    @staticmethod
    def cat_tab_put(tab_cat_name):
        command = list()
        command.append('CALL FUNCTION \'DDIF_TTYP_PUT\'')
        command.append('EXPORTING')
        command.append('name = \'Y' + tab_cat_name + '\'')
        command.append('dd40v_wa          = wa_dd40v')
        command.append('EXCEPTIONS')
        command.append('ttyp_not_found    = 1')
        command.append('name_inconsistent = 2')
        command.append('ttyp_inconsistent = 3')
        command.append('put_failure       = 4')
        command.append('put_refused       = 5')
        command.append('OTHERS = 6.')
        command.append('IF sy-subrc <> 0.')
        command.append('MESSAGE ID sy-msgid TYPE sy-msgty NUMBER sy-msgno WITH sy-msgv1 sy-msgv2 sy-msgv3 sy-msgv4.')
        command.append('ENDIF.')
        return command

    @staticmethod
    def cat_tab_activate(tab_cat_name):
        command = list()
        command.append('CALL FUNCTION \'DDIF_TTYP_ACTIVATE\'')
        command.append('EXPORTING')
        command.append('name        = \'Y' + tab_cat_name + '\'')
        command.append('EXCEPTIONS')
        command.append('not_found   = 1')
        command.append('put_failure = 2')
        command.append('OTHERS      = 3.\n')
        command.append('IF sy-subrc <> 0.')
        command.append('MESSAGE ID sy-msgid TYPE sy-msgty NUMBER sy-msgno WITH sy-msgv1 sy-msgv2 sy-msgv3 sy-msgv4.')
        command.append('ENDIF.\n')
        command.append('CLEAR wa_dd40v.')
        return command

    @staticmethod
    def struct_line(tab_name, field_name, type_name, position):
        # type: (str,str,str,int) -> [str]

        if not DataStructure.basic_types.__contains__(type_name):
            type_name = 'Y' + type_name

        command = list()
        command.append('CLEAR idd03p.')
        command.append('idd03p-tabname  = \'Y' + tab_name + '\'.')
        command.append('idd03p-fieldname = \'' + field_name + '\'.')
        command.append('idd03p-rollname = \'' + type_name + '\'.')
        command.append('idd03p-position = \'' + str(position) + '\'.')
        command.append('APPEND idd03p.')
        return command

    @staticmethod
    def struct_def(tab_name, description):
        # type: (str,str,str,str,str) -> [str]
        command = list()
        command.append('xdd02v-tabname = \'Y' + tab_name + '\'.')
        command.append('xdd02v-tabclass = \'INTTAB\'.')
        command.append('xdd02v-ddlanguage =  sy-langu.')
        command.append('xdd02v-langdep =  sy-langu.')
        command.append('xdd02v-ddtext  = \'' + description + '\'.')
        return command

    @staticmethod
    def tabl_put(tab_name):
        # type: (str) -> [str]
        command = list()
        command.append('CALL FUNCTION \'DDIF_TABL_PUT\'')
        command.append('EXPORTING')
        command.append('name = \'Y' + tab_name + '\'')
        command.append('dd02v_wa          = xdd02v')
        command.append('TABLES')
        command.append('dd03p_tab         = idd03p')
        command.append('EXCEPTIONS')
        command.append('tabl_not_found    = 1')
        command.append('name_inconsistent = 2')
        command.append('tabl_inconsistent = 3')
        command.append('put_failure       = 4')
        command.append('put_refused       = 5')
        command.append('OTHERS            = 6.\n')
        command.append('IF sy-subrc <> 0.')
        command.append('MESSAGE ID sy-msgid TYPE sy-msgty NUMBER sy-msgno WITH sy-msgv1 sy-msgv2 sy-msgv3 sy-msgv4.')
        command.append('ENDIF.')
        return command

    @staticmethod
    def tabl_activate(tab_name):
        command = list()
        command.append('CALL FUNCTION \'DDIF_TABL_ACTIVATE\'')
        command.append('EXPORTING')
        command.append('name        = \'Y' + tab_name + '\'')
        command.append('EXCEPTIONS')
        command.append('not_found   = 1')
        command.append('put_failure = 2')
        command.append('OTHERS      = 3.\n')
        command.append('IF sy-subrc <> 0.')
        command.append('MESSAGE ID sy-msgid TYPE sy-msgty NUMBER sy-msgno WITH sy-msgv1 sy-msgv2 sy-msgv3 sy-msgv4.')
        command.append('ENDIF.\n')
        command.append('CLEAR idd03p[].')
        return command
