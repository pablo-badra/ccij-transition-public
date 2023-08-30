import pandas as pd
import numpy as np
import datetime as dt
import os

def create():
    def open_file_1(file):
        file = pd.read_csv(
            cwd+'data/raw_csv_files/data_set/'+str(file)+'.csv',
            header=0, index_col='caseregisters_id')
        file = file.loc[~file.index.duplicated(),:]

        return file

    def open_file_2(file):
        try: 
            file = pd.read_csv(
                cwd+'data/raw_csv_files/data_set/'+str(file)+'.csv',
                header=0, index_col='record_id',usecols=['record_id', str(file)])
            file = file.loc[~file.index.duplicated(),:]
        except ValueError:
            print(file)
        return file

    def fix_caseaction_id(df):
        dic = {'MVDF KYR - Detention Visit (Centro)':'@MVDF','Golden State KYR - Golden State Detention Visits':'@Golden State', 'DUBLIN - IHP Dublin':'@Dublin','AB32 MVDF - AB32 Coordination':'@MVDF'}
        for x in df[df.caseaction_id.isna()].index:
            try:
                df.loc[x,'caseaction_id'] = dic[df.loc[x,'casetype_id']]
            except KeyError:
                pass
        return df

    def age_open(df):
        z = []
        for x, y in df.lawlab_opened.items():
            date = y
            bday = df['DOB'][x]
            age = date.year - bday.year - ((date.month, date.day) < (bday.month, bday.day))
            z.append(age)
        return z

    def calculateRace(df):
        api = ['Vietnamese','Koreans','Japanese','Tajiks','Hindustani']
        white = ['Russians','Portuguese','English','Moldovans','Romanians','Ukrainians','Armenians']
        black = ['Garifuna']
        latinx = ['Latino']
        other = ['Arabs', 'Lebanese']
        dapic = []
        dwhite = []
        dblack = []
        dlatinx = []
        dother = []
        to_keep = []
        race_to_keep = ['American Indian or Alaska Native', 'Black or African American', 'Asian', 'Native Hawaiian or Pacific Islander', 'White']
        race_to_replace = {'American Indian or Alaska Native':'Indigenous', 'Black or African American':'Black', 'Native Hawaiian or Pacific Islander':'Asian/Pacific Islander', 'Asian':'Asian/Pacific Islander'}
        for x, y in df['race'].items():
            if y in race_to_keep:
                to_keep.append(x)
            else:
                pass

        df.replace(to_replace=race_to_replace, value=None, inplace=True)

        for x, y in df['ethnicity'].items():
            if x in to_keep:
                pass
            else:
                if y in api:
                    print((str(df['ethnicity'][x]) + ' and ' + str(df['race'][x]))  + ' converted to ' + 'Asian/Pacific Islander' + ' index= ' + str(x))
                    dapic.append(x)
                elif y in white:
                    print((str(df['ethnicity'][x]) + ' and ' + str(df['race'][x]))  + ' converted to ' + 'White' + ' index= ' + str(x))
                    dwhite.append(x)
                elif y in black:
                    print((str(df['ethnicity'][x]) + ' and ' + str(df['race'][x]))  + ' converted to ' + 'Black' + ' index= ' + str(x))
                    dblack.append(x)
                elif y in latinx:
                    print((str(df['ethnicity'][x]) + ' and ' + str(df['race'][x]))  + ' converted to ' + 'Latino' + ' index= ' + str(x))
                    dlatinx.append(x)
                elif y in other:
                    print((str(df['ethnicity'][x]) + ' and ' + str(df['race'][x]))  + ' converted to ' + 'Other' + ' index= ' + str(x))
                    dother.append(x)
                elif y == 'Hispanic' and type(df['race'][x]) != str:
                    # print((str(df['ethnicity'][x]) + ' and ' + str(df['race'][x]))  + ' converted to ' + 'Latinx')
                    dlatinx.append(x)

        for x in dapic:
            df.loc[x, 'race'] = 'Asian/Pacific Islander'
        for x in dwhite:
            df.loc[x, 'race'] = 'White'
        for x in dblack:
            df.loc[x, 'race'] = 'Black'
        for x in dlatinx:
            df.loc[x, 'race'] = 'Latinx'
        for x in dother:
            df.loc[x, 'race'] = 'Other'

        return df



    cwd = os.getcwd().strip('python_files')

    files = ['opened','closed','adelanto','dublin','gsa','imperial','mvdf','otaymesa','yuba']
    opened, closed, adelanto, dublin, gsa, imperial, mvdf, otaymesa, yuba = [open_file_1(x) for x in files]
    cases = pd.concat([opened,closed])
    cases = cases.loc[~cases.index.duplicated(),:]
    cases = cases[cases['opened']>='2020-01-01']
    dcs = [adelanto, dublin, gsa, imperial, mvdf, otaymesa, yuba]
    dcs = pd.concat(dcs)
    dcs = dcs['caseaction_id']
    df = cases.merge(dcs, on=['caseregisters_id'])
    not_cases = cases.loc[~cases.index.isin(df.index),:]
    df = pd.concat([df,not_cases])
    df = df.drop_duplicates(subset='record_id',keep='first')
    df = fix_caseaction_id(df)
    df = df.set_index('record_id')
    cols = ['gender_id','DOB','aNum','birth_country_id','address','city','county','state','zip','language_id','race','ethnicity','immigration_status_id','initiated_date', 'phone_owner', 'phone']
    gender_id, DOB, aNum, birth_country_id, address, city, county, state, zip, language_id, race, ethnicity, immigration_status_id, initiated_date, phone_owner, phone = [open_file_2(x) for x in cols]
    cols_ser = [gender_id, DOB, aNum, birth_country_id, address, city, county, state, zip, language_id, race, ethnicity, immigration_status_id, initiated_date, phone_owner, phone]
    df = df.join(cols_ser)
    colsStr = ["aNum", "address", "city", "county", "state", "zip", "gender_id", "DOB", "birth_country_id", "ethnicity", "race", "language_id", "immigration_status_id", "initiated_date", "pob", "phone_owner", "phone"]
    corCol = {'opened':'lawlab_opened', 'firstName':'first_name', 'lastName':'last_name', 'caseaction_id':'cohort', 'aNum':'a_number', 'gender_id':'gender', 'birth_country_id':'country_of_birth', 'language_id':'language', 'immigration_status_id':'immigration_status', 'initiated_date':'date_detained', 'closed':'lawlab_closed', 'comment':'transfers', 'casetype_id':'casetype', 'phone_owner':'contact_name', 'phone':'contact_phone'}
    corCity = {'Pamona': 'Pomona', 'Azuza': 'Azusa', 'Monte': 'El Monte', 'El Puente': 'La Puente', 'Santa Barbera': 'Santa Barbera', 'San Francico': 'San Francisco', 'Anahaim': 'Anaheim', 'Colinga': 'Coalinga', 'Westminister': 'Westminster', 'Fondana': 'Fontana', 'Vajello': 'Vallejo', 'Pittsburgh': 'Pittsburg','San Jose / Milpitas':'San Jose'}
    corCountry = {'CHINA':'China, Peoples Republic of', "LAO PEOPLE'S DEMOCRATIC REPUBLIC":'Laos', 'MOLDOVA, REPUBLIC OF':'Moldova', 'AMERICAN SAMOA':'SAMOA', 'CZECH REPUBLIC':'Czechia (Czech Republic)'}
    cor_ice_country = {'CHINA':'China, Peoples Republic of', "LAO PEOPLE'S DEMOCRATIC REPUBLIC":'Laos', 'MOLDOVA, REPUBLIC OF':'Moldova', 'AMERICAN SAMOA':'Samoa', 'Czechia (Czech Republic)':'Czech Republic', 'AZERBAIJAN':'Azerbaijan','TAIWAN, PROVINCE OF CHINA':'Taiwan', 'VIRGIN ISLANDS, BRITISH':'British Virgin Islands','SRI LANKA':'Sri Lanka','MARSHALL ISLANDS':'Marshall Islands',"KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF":'North Korea','PALESTINIAN TERRITORY, OCCUPIED':'ISRAEL'}
    corCohort = {'@Golden State':'Golden State Annex', '@MVDF':'Mesa Verde Detention Facility', '@Yuba':'Yuba County Detention Facility', '@Dublin':'FCI Dublin', '@Imperial':'Imperial Regional Detention Center','@Otay Mesa':'Otay Mesa Detention Center', '@Adelanto':'Adelanto Detention Facility'}
    corImm = {'No Lawful Status / No Estatus Legal':'Undocumented', 'LPR (Lawful Permanent Resident) / (Residente Legal Permanente)':'LPR', 'Unknown / Desconocidx':'Unknown', 'Other / Otro':'Other', 'Asylee / Asiladx':'Asylee'}
    corGender = {'Non-binary':'Nonbinary'}
    corCasetype = {'Golden State KYR - Golden State Detention Visits':'GSA-KYR', 'MVDF KYR - Detention Visit (Centro)':'Partner Intake', 
                   'AOD - Detained Attorney of the Day':'AOD/Courtwatch', 'CCIJ Yuba KYR - Yuba Detention Visits':'Yuba-KYR', 'Hotline - CCIJ Hotline Calls':'Direct Contact',
                   'RO-VD (AOD) - AOD Removals/Voluntary Departure':'AOD/Courtwatch', 'Referrals - Referrals to CCIJ':'Referral', 'RAPID RESPONSE - Regional Rapid Response':'Rapid Response',
                   'AB32 MVDF - AB32 Coordination':'Partner Intake', 'SFPD - SF Public Defender':'Partner Intake','DUBLIN - IHP Dublin':'Partner Intake',
                  'Other ICE Detention - ICE Detention other than Yuba/MVDF/GSA':'Other', 'Rmvl Defense-Other - Termination, Suppression, etc.':'Other','Removal Defense-Bond - Bond Hearing':'Other', 'Release Request-ICE - Parole, OR, etc.':'Other', 'Rmvl Defense-Asylum - Asylum, W/H, CAT':'Other', 'CFI/RFI - Credible or Reasonable Fear Interview':'Other','BIA - BIA Appeal':'Other', 'Affirmative AOS - AOS with USCIS':'Other'}
    corCounty = {'San Bernadino':'San Bernardino'}
    df = df.rename(mapper=corCol, axis=1)
    df['a_number'] = df['a_number'].astype('str')

    df['county']=df['county'].str.title()
    df['county'] = df['county'].where(df['county']!="Unknown")
    df['city']=df['city'].str.title()
    df['zip']=df['zip'].astype('str')

    df.loc[~df.county.isna(),'county'] = df.loc[~df.county.isna(),'county'].replace(to_replace='(\s+County)', value='', regex=True).replace(to_replace='(\s+County)', value='', regex=True)

    df['city'].replace(to_replace=corCity, value=None, inplace=True)
    df['county'].replace(to_replace=corCounty, value=None, inplace=True)
    df['country_of_birth'].replace(to_replace=corCountry, value=None, inplace=True)
    df['ice_country_of_birth'] = df['country_of_birth'].replace(to_replace=cor_ice_country, value=None)
    df['cohort'].replace(to_replace=corCohort, value=None, inplace=True)
    df['immigration_status'].replace(to_replace=corImm, value=None, inplace=True)  
    df['gender'].replace(to_replace=corGender, value=None, inplace=True)
    df['casetype'].replace(to_replace=corCasetype, value=None, inplace=True)
    df['presumed_detained'] = df['lawlab_closed']
    df['presumed_detained'].replace(to_replace=r'(.+)', value=False, inplace=True, regex=True)
    df['presumed_detained'].fillna(value=True, inplace=True)

    df['lawlab_opened'] = pd.to_datetime(df['lawlab_opened'])
    df['DOB'] = pd.to_datetime(df['DOB'])
    df['age_at_open'] = age_open(df)

    df = calculateRace(df)
    cn = pd.read_csv(cwd+'data/raw_csv_files/data_set/casenote.csv')
    cn.drop_duplicates(subset='record_id', keep='first', inplace=True)
    cn = cn[cn['comment'].str.contains(pat=r'(?i)(?i)in\Wp\wrs\wn\Wclinic|ipc', regex=True, na=False)]
    ipc = cn.record_id.values.astype('str')
    df = df.reset_index()
    df.record_id = df.record_id.astype(str)
    df[df['casetype']=='GSA-KYR']['casetype'] = 'Remote Clinic'
    df.casetype.replace(to_replace='GSA-KYR',value='Remote Clinic', inplace=True)
    df.loc[df['record_id'].isin(ipc),'casetype'] = 'In Person Clinic'
    yc = df[df['casetype']=='Yuba-KYR']
    yipc = yc[yc['lawlab_opened']<'2020-03-01']
    yipc = yipc.record_id.values
    yrc = yc[yc['lawlab_opened']<'2022-09-01']
    yrc = yrc[yrc['lawlab_opened']>'2020-3-01']
    yrc = yrc.record_id.values
    ypi = yc[yc['lawlab_opened']>'2022-09-01']
    ypi = ypi.record_id.values
    df.loc[df['record_id'].isin(yipc),'casetype'] = 'In Person Clinic'
    df.loc[df['record_id'].isin(yrc),'casetype'] = 'Remote Clinic'
    df.loc[df['record_id'].isin(ypi),'casetype'] = 'Partner Intake'
    df.drop('party_id', axis=1,inplace=True)
    df.drop(labels=['address', 'ethnicity','age_at_open'], axis=1, inplace=True)
    fn1 =cwd+'data/exported_files/dataset/export_'+pd.to_datetime('today').strftime('%Y-%m-%d')+'.csv'
    fn2 =cwd+'data/exported_files/dataset/export.csv'
    df.to_csv(fn1)
    df.to_csv(fn2)
    return df

###

###

def extref():
    def open_file_1(file):
        file = pd.read_csv(
            cwd+'data/raw_csv_files/data_set/'+str(file)+'.csv',
            header=0, index_col='caseregisters_id')
        file = file.loc[~file.index.duplicated(),:]

        return file

    def open_file_2(file):
        try: 
            file = pd.read_csv(
                cwd+'data/raw_csv_files/data_set/'+str(file)+'.csv',
                header=0, index_col='record_id',usecols=['record_id', str(file)])
            file = file.loc[~file.index.duplicated(),:]
        except ValueError:
            print(file)
        return file

    def fix_caseaction_id(df):
        dic = {'MVDF KYR - Detention Visit (Centro)':'@MVDF','Golden State KYR - Golden State Detention Visits':'@Golden State', 'DUBLIN - IHP Dublin':'@Dublin','AB32 MVDF - AB32 Coordination':'@MVDF'}
        for x in df[df.caseaction_id.isna()].index:
            try:
                df.loc[x,'caseaction_id'] = dic[df.loc[x,'casetype_id']]
            except KeyError:
                pass
        return df



    cwd = os.getcwd().strip('python_files')

    files = ['opened','closed','adelanto','dublin','gsa','imperial','mvdf','otaymesa','yuba']
    opened, closed, adelanto, dublin, gsa, imperial, mvdf, otaymesa, yuba = [open_file_1(x) for x in files]
    cases = pd.concat([opened,closed])
    cases = cases.loc[~cases.index.duplicated(),:]
    cases = cases[cases['opened']>='2020-01-01']
    dcs = [adelanto, dublin, gsa, imperial, mvdf, otaymesa, yuba]
    dcs = pd.concat(dcs)
    dcs = dcs['caseaction_id']
    df = cases.merge(dcs, on=['caseregisters_id'])
    not_cases = cases.loc[~cases.index.isin(df.index),:]
    df = pd.concat([df,not_cases])
    df = df.drop_duplicates(subset='record_id',keep='first')
    df = fix_caseaction_id(df)
    #df = df.set_index('record_id')
    df.drop(labels=['address', 'ethnicity','age_at_open'], axis=1, inplace=True)
    fn1 =cwd+'data/exported_files/dataset/export_'+pd.to_datetime('today').strftime('%Y-%m-%d')+'.csv'
    fn2 =cwd+'data/exported_files/dataset/export.csv'
    df.to_csv(fn1)
    df.to_csv(fn2)
    return df