import traceback
from django.core.paginator import Paginator
from django.core.management.base import BaseCommand, CommandError
from voyages.apps.voyage import models, legacy_models
from decimal import *
import sys
import unidecode
from optparse import make_option
#def short_ref_matches(short_ref, text_ref):
#    return short_ref and text_ref and short_ref.replace(' ','') == text_ref.replace(' ','')

def find_by_value(vlist, value):
    # This will error when there is not a matching entry in the dictionary.
    # That is on purpose since that indicates probable missing/corrupted data
    return vlist[value]
    #return filter(lambda x: x.value == value, vlist)[0]

# This is an auto generated dictionary that is outputted by the script listsourcefixes
source_fix_dict = {u'Vila Vilar, 258-59': u'Vila Vilar, 258-59', u'Hernaes,275,287': u'Hernaes,275,287', u'Post ManandtheHistorical Account (London),96.06.26': u'Post ManandtheHistorical Account (London),96.06.26', u'PublicAdvertiser,62.01.14.': u'PublicAdvertiser,62.01.14.', u'VilaVilar,Cuadro3, 260-61': u'VilaVilar,Cuadro3, 260-61', u'Adm1/2719, #231': u'ADM1/2719, #231"', u'RIHS,microf,reel12/24,brig"Punch"': u'RIHS,microf,reel12/24,brig"Punch"', u"Lloyd's Evening Post, 64.07.25.": u"Lloyd's Evening Post, 64.07.25", u'Gelpi Baiz, 222': u'Gelpi Baiz, 222', u"St.James'sChronicle,1778.02.21.": u"St.James'sChronicle,1778.02.21.", u'SL,LAR,10115-15143,12571-12597': u'SLA,LAR,10115-15143,12571-12597', u'VilaVilar, Cuadro 3, 258-59': u'VilaVilar, Cuadro 3, 258-59', u'PublicAdvertiser,54.08.27.': u'PublicAdvertiser,54.08.27.', u'Jctp, 50-53': None, u'Proc. of Old Bailey, ref t17250630-58': u'Proc. of Old Bailey, ref t17250630-58', u'HLB,8:379-87': None, u'StJamesChronicle,1775.11.17.': u'StJamesChronicle,1775.11.17.', u'DailyNationalIntelligencer,1820.06.13.': u'DailyNationalIntelligencer,1820.06.13', u'Vila Vilar, 170, n. 48': u'Vila Vilar, 170, n. 48', u'Paesie,305': u'Paesie,305', u'Borrego Pla, 59': u'Borrego Pla, 59', u'Borrego Pla, 58': u'Borrego Pla, 58', u'Barcia dataset': u'BarciaDataset"', u'Farias,1983,II': u'Farias, 1983, II: 149', u"Freeman's Journal,1780.06.01,p.2": u"Freeman's Journal,1780.06.01,p.2", u'Vila Vilar, 268-69': u'Vila Vilar, 268-69', u'Norregard,61': u'Norregard,61', u'Szymanski,76': u'Szymanski,76', u'Norregard,64': u'Norregard,64', u'Radburn,48': u'Radburn,48', u'Radburn,49': u'Radburn,49', u'Guerard': u'Guerard', u'Farley?s,68.04.16.': u"Farley's,68.04.16", u'schofield,268': u'Schofield,268', u'Vila Vilar, 174, 276-77': u'Vila Vilar, 174, 276-77', u'Norregard,122': u'Norregard,122', u'Radburn,46': u'Radburn,46', u'Vila Vilar, Cuadro 3, 258-59': u'Vila Vilar, Cuadro 3, 258-59', u'Paesie,291': u'Paesie,291', u'Vila Vilar, Cuadro 2, 252-53': u'Vila Vilar, Cuadro 2, 252-53', u'British Journal (London), 1723.01.05.': u'British Journal (London), 1723.01.05', u'ANG-U, EGH 40, 87': u'ANGU, EGH 40, 87"', u'Pleitos, Audiencia de Santo Domingo, 1581-1582 ': u'AGI,Escribania 2A, pieza 2, folios 1r-825v.', u'VilaVilar, p. 173': u'VilaVilar, p. 173', u'Hernaes,205-6': u'Hernaes,205-6', u'Norregard,81': u'Norregard,81', u'Post Boy,24.07.1719': u'Post Boy,24.07.1719', u'Hernaes,256-257': u'Hernaes,256-257', u"StJames'sChronicle,67.05.14.": u"StJames'sChronicle,67.05.14.", u'SL,LAR,11909-15967,12571-12597': u'SLA,LAR,11909-15967,12571-12597', u'Vila Vilar, 248-49': u'Vila Vilar, 248-49', u'Farias,1983,II,149': u'Farias,1983,II,149', u'St.JamesChronicle,69.10.07.': u'St.JamesChronicle,69.10.07.', u'Paesie,308': u'Paesie,308', u'Norregard,Madagascar': u'Norregard,Madagascar', u'Post Boy,06.11.05.': u'Post Boy,06.11.05', u'Kew, CO247/97, 63.07.11.': u'CO247/97, 63.07.11', u'Vila Vilar, 174-75, 276-77': u'Vila Vilar, 174-75, 276-77', u'Gazetteer and London Daily Advertiser,1756.10.16.': u'Gazetteer and London Daily Advertiser,1756.10.16', u'D/DAV/1': u'MMM/D/DAV/1', u'Daily Post (London), 1729.05.29.': u'Daily Post, 1729.05.29', u'Norregard,67-68': u'Norregard,67-68', u'Norregard,71': u'Norregard,71', u'Norregard,124-5': u'Norregard,124-5', u'Norregard,72': u'Norregard,72', u'n.1 (1575), ff. 13r, 32r-33r; n.1 (1577), f. 18v': u'AGI,Contaduria,1052, n.1 (1575), ff. 13r, 32r-33r; n.1 (1577), f.18v', u'Paesie,130': u'Paesie,130', u'Dawk?s, December 15, 1713': u"Dawk's, December 15, 1713", u'VilaVilar,142': u'VilaVilar,142', u'Norregard,78': u'Norregard,78', u'Farias, 1986, 254': u'Farias, 1986, 254', u'FelixFarley, 83.06.21.': u"Farley's, 83.06.21", u'Norregard,115': u'Norregard,115', u'http://www.stg.brown.edu/projects/sally/': u'Sally', u'VilaVilar, Cuadro3, 264-65': u'VilaVilar, Cuadro3, 264-65', u'Weekly Packet (London),1719.12.26.': u'Weekly Packet (London),1719.12.26.', u'Gelpi Baiz, 224, 338, fn. 43': u'Gelpi Baiz, 224, 338, fn. 43', u'Hernaes, 256,259': u'Hernaes, 256,259', u'ANTT,JuntaComercio,Lv.74:147v': u'ANTT,JC,Lv.74:147v', u'Stoddart': None, u'WeeklyJamaicaCourant,18.07.30.': u'WeeklyJamaicaCourant,18.07.30.', u'StJamesChronicle,67.05.14.': u'StJamesChronicle,67.05.14.', u'Walsh,II,262': u'Walsh,II,262', u'Norregard,88': u'Norregard,88', u'Public Advertiser, 81.08.10.': u'Public Advertiser, 81.08.10.', u'Paesie,130,308-09': u'Paesie,130,308-09', u'VilaVilar,Cuadro5': u'VilaVilar,Cuadro5', u'BaggeAcctBook': u'BaggeAcctBook', u'Norregard,82': u'Norregard,82', u'VilaVilar,Cuadro6': u'VilaVilar,Cuadro6', u'Studnicki-Gizbert (2007), 60, 197n102': u'Studnicki-Gizbert (2007), 60, 197n102', u'DailyNationalIntelligencer,1820.06.19.': u'DailyNationalIntelligencer,1820.06.19', u'VilaVilar,Cuadro3': u'VilaVilar,Cuadro3', u"Robert Hibbert's diary": u"Robert Hibbert's diary", u'Hernaes,273': u'Hernaes,273', u'Boeseken,143': u'Boeseken,143', u'Daily Advertiser, 31.07.07.': u'Daily Advertiser, 31.07.07', u'Radburn,63': u'Radburn,63', u'Farley?s,73.12.04.': u"Farley's,73.12.04", u'Vila Villar, 1977, p. 171, fn. 52': u'Vila Vilar, 1977, p. 171, fn. 52', u'ADG, 2L, No 206, Actes Notariels,1797-1802': u'ADG, 2L, No 206, Actes Notariels,1797-1802', u'Norregard,66,89': u'Norregard,22,89', u'Hernaes,271,285': u'Hernaes,271,284', u'Hernaes,271,284': u'Hernaes,271,284', u'Hernaes,206,265': u'Hernaes,206,265', u'GUS,1800.08.21.': None, u'Farias, 1986, 152': u'Farias, 1986, 152', u'Norregard,Slaveoproret': u'Norregard,Slaveoproret', u'Norregard,102': u'Norregard,102', u'Norregard,114': u'Norregard,114', u'Norregard,104': u'Norregard,104', u'SL,LAR, register 7508-9758, 9208-9456': u'SLA,LAR, register 7508-9758, 9208-9456', u'Norregard,107': u'Norregard,107', u'Norregard,108': u'Norregard,108', u'Norregard,109': u'Norregard,109', u'Szymanski,65-6,76': u'Szymanski,65-6,76', u'Klein,Havana data-set,1790-1820': u'Klein,Havana data-set,1790-1820', u'VilaVilar,174': u'VilaVilar,174', u'Norregard,124-5,128': u'Norregard,124-5,128', u'FHL,Reel88789,Williams': u'FHL,Reel88789,Williams', u'Hernaes,263-268': u'Hernaes,263-268', u'Hernaes,269,284': u'Hernaes,269,284', u'Farley?s,73.12.11.': u"Farley's,73.12.11", u'Norregard,111': u'Norregard,111', u'Hernaes,251': u'Hernaes,251', u'Remembrancer,49.03.17': u'Remembrancer,49.03.17', u'VilaVilar,Cuadro3, 256-57': u'VilaVilar,Cuadro3, 256-57', u'P,1840,XLVI:67': u'PP,1840,XLVI:67', u'Hernaes,272,273': u'Hernaes,272,273', u'RIHS,USCust,C#1,Dec,1801-2,Cert #24': u'RIHS,USCust,C#1,Dec,1801-2,Cert #24', u'2884, Series 2, no 7.': u'AGI, Contrataci\xf3n, Legajo 2884, Series 2, no 7.', u'VilaVilar,100': u'VilaVilar,100', u'James Stewart, Reports of Cases, 219-20': u'James Stewart, Reports of Cases, 219-20', u'Vila Vilar, Cuadro 4': u'Vila Vilar, Cuadro 4', u'Vila Vilar, Cuadro 3, 260-61': u'Vila Vilar, Cuadro 3, 260-61', u'MassHistSoc,8:337': u'MassHistSoc,8:337', u'Post Man,10.05.02.': u'Post Man,10.05.02.', u'Newson, Minchon, 65': u'Newson, Minchin2, 65', u'Raw,C747,170,212,216': u'Rawl,C747,170,212,216', u'Farley?s,68.03.12.': u"Farley's,68.03.12", u'dg, 9 Feb 1805': u'dg, 9 Feb 1805', u'Acosta Saignes, 33': u'Acosta Saignes, 1961, 33', u'Hernaes,270,284': u'Hernaes,270,285', u'Hernaes,270,285': u'Hernaes,270,285', u'Brasio, MMA, 2a Serie, III: 207-10': u'MMA, 2a Serie, III: 207-10', u'Hernaes,272,285': u'Hernaes,272,285', u'VilaVilar, p.173': u'VilaVilar, p.173', u'Acosta Saignes, 38': u'Acosta Saignes, 1961, 38', u'Public Advertizer, 54.07.06.': u'Public Advertizer, 54.07.06.', u'  .': None, u'Farias, 1983, 149': u'Farias, 1983, II: 149', u'Prior,pp. 12-13': u'Prior,pp. 12-13', u'Boeseken,140-41': u'Boeseken,140-41', u'Hernaes,256,259': u'Hernaes,256,259', u'Hernaes,256,258': u'Hernaes,256,258', u'Lobo Cabrera (1990), 358': u'Lobo Cabrera (1990), 358', u'http://www.cslib.org/slaverlog.htm': u'http://www.cslib.org/slaverlog.htm', u'DailyCourant,28.04.22.': u'DailyCourant,28.04.22', u'MMM,DX/1304': u'MMM,DX/1304', u'Vila Vilar, Cuadro 3, 256-7': u'Vila Vilar, Cuadro 3, 256-7', u'DailyNationalIntelligencer,1821.08.02.': u'DailyNationalIntelligencer,1821.08.02', u'World and Fashionable Advertiser, 1787.09.22.': u'World and Fashionable Advertiser, 1787.09.22.', u'RRNCW,1806.07.07.': u'RRNCW,1806.07.07.', u'Norregard,67-68,89': u'Norregard,67-68,89', u'Hernaes,256,258-259': u'Hernaes,256,258-259', u'Paesie,323': u'Paesie,323', u'JA,SpanishTown,1B/5/13/1,OutLetters,June,1793': u'JA,SpanishTown,1B/5/13/1,OutLetters,June,1793', u'Norregard,99': u'Norregard,99', u'Vila Vilar, Cuadro 2, 254-255': u'Vila Vilar, Cuadro 2, 254-255', u"StJames'sChronicle,65.03.02.": u"StJames'sChronicle,65.03.02.", u'VilaVilar,Cuadro6, 278-79': u'VilaVilar,Cuadro6, 278-79', u'VilaVilar,132': u'VilaVilar,132', u'Denman, 17-21': u'Denman, 17-21', u'Farias,II': u'Farias, 1983, II: 149', u'VilaVilar, Cuadro3, 260-61': u'VilaVilar, Cuadro3, 260-61', u'Vila Vilar, 170, n 48': u'Vila Vilar, 170, n 48', u'HarpersWeekly,60.06.02.': u'HarpersWeekly,60.06.02', u'Vila Vilar, 260-1': u'Vila Vilar, 260-1', u'Acosta Saignes, 79, 99': u'Acosta Saignes, 1967, 79, 99', u'VilaVilar,94,C6': u'VilaVilar,94,C6', u"St.James'sChronicle/British Evening Post,61.04.23.": u"St.James'sChronicle/British Evening Post,61.04.23.", u'Hernaes,205-206': u'Hernaes,205-206', u'Farley?s,73.10.16.': u"Farley's,73.10.16", u'General Evening Post, 1788.01.08.': u'General Evening Post, 1788.01.08.', u'VilaVilar,192': u'VilaVilar,192', u'LDPGA, 40.04.29.': u'LDPGA, 40.04.29.', u'Farias, 1983, 151': u'Farias, 1983, II: 151', u'Hernaes,257,260': u'Hernaes,257,260', u'Vila Vilar, Cuadro 2': u'Vila Vilar, Cuadro 2', u'.': None, u'Norregard,76': u'Norregard,76', u"StJames'sChronicleortheBritishEvenPost,1766.07.29": u"StJames'sChronicleortheBritishEvenPost,1766.07.29.", u'Farias, 1986, 289': u'Farias, 1986, 289', u'Farias, 1986, 288': u'Farias, 1986, 288', u'Farias, 1986, 287': u'Farias, 1986, 287', u'Farias, 1986, 285': u'Farias, 1986, 285', u'Hernaes,188-89': u'Hernaes,188-89', u'Farias, 1986, 283': u'Farias, 1986, 283', u'Farias, 1986, 282': u'Farias, 1986, 282', u'Norregard,64-65': u'Norregard,64-65', u'Farley?s,68.01.02.': u"Farley's,68.01.02", u'Hernaes,251-252': u'Hernaes,251-252', u'Farias, 264': u'Farias, 1986, 264', u'Dawk?s, November 28, 1713': u"Dawk's, November 28, 1713", u'D?Auvergne,73-4': u"D'Auvergne,73-4", u'National Advocate,1816.07.01.': u'National Advocate,1816.07.01.', u'Hernaes,194': u'Hernaes,194', u'DailyNationalIntelligencer,1821.08.23.': u'DailyNationalIntelligencer,1821.08.23', u'D?Elbee,477': u"D'Elbee,477", u'D?Elbee': u"D'Elbee", u'Hildebrand, Ingegerd, "Svenska Kolonin,"pp. 226-27': u'Hildebrand, Ingegerd, "Svenska Kolonin," pp. 226-27', u'O?Callaghan,Voyages': u"O'Callaghan,Voyages", u'Briceno-Iragorry, II (1600-1605), 153-57': u'Brice\xf1o Iragorry, II (1600-1605), 153-57', u'Norwich Gazette, 41.10.17.': u'Norwich Gazette, 41.10.17.', u'PublicAdvertiser,54.07.12.': u'PublicAdvertiser,54.07.12.', u'VilaVilar,Cuadro2': u'VilaVilar,Cuadro2', u'BRO,P/Xch/D/23,1738.04.26': u'BRO,P/Xch/D/23,1738.04.26', u'Hernaes,273,286': u'Hernaes,273,286', u'Sua Majestad,www.african-origins.org': u'Sua Majestad,www.african-origins.org', u'Dawk?s, December 5, 1713': u"Dawk's, December 5, 1713", u"Freeman's Journal,1787.12.13.": u"Freeman's Journal,1787.12.13", u'StJamesChronicle,65.07.30.': u'StJamesChronicle,65.07.30.', u'Hernaes,261': u'Hernaes,261', u'DonganPapers,I:171-72,270-72': u'DonganPapers,I:171-72,270-72', u'Farley?s,49.01.07.': u"Farley's,49.01.07", u'DailyCourant,28.04.25.': u'DailyCourant,28.04.25', u'Hernaes,164-165': u'Hernaes,164-165', u'Hernaes,269': u'Hernaes,269', u'Hernaes,278': u'Hernaes,278', u'HMM,52.05.19.': u'HMMGA,52.05.19', u'Paesie,287': u'Paesie,287', u'Farley?s,74.12.03.': u"Farley's,74.12.03", u'VilaVilar,p. 173': u'VilaVilar,p. 173', u'Norregard,50': u'Norregard,50', u'Vila Vilar, Cuadro 3, 256-57': u'Vila Vilar, Cuadro 3, 256-57', u'Vila Vilar, 260-61': u'Vila Vilar, 260-61', u'VilaVilar, Cuadro3': u'VilaVilar, Cuadro3', u'Santo Domingo, 55, Ramo 19, number 104, doc. 1, 1 Mar 1639. ': u'AGI,Santo Domingo, 55, Ramo 19, number 104, doc. 1, 1 Mar 1639', u'Public Advertiser, 81.07.12.': u'Public Advertiser, 81.07.12.', u'Norregard,116': u'Norregard,116', u'VilaVilar, 250-51': u'VilaVilar, 250-51', u'Hernaes,189': u'Hernaes,189', u'Maria Paul, www.african-origins.org': u'Maria Paul, www.african-origins.org', u"Baldwin's London Weekly Journal,1788.05.13.": u"Baldwin's London Weekly Journal,1788.05.13", u'Vila Vilar, 276-77': u'Vila Vilar, 276-77', u'Weekly Packet (London), 1719.12.26.': u'Weekly Packet (London), 1719.12.26.', u'MMHGA,62.09.14.': u'MMHGA,62.09.14.', u'MorningHeraldandDailyAdvertiser,83.09.04.': u'MorningHeraldandDailyAdvertiser,83.09.04.', u'Farley?s,June2,1754': u"Farley's,June2,1754", u'2 Dobson 413 (Dec. 10, 1819)': u'Dodson2,p.413 (Dec. 10 1819)', u'Hernaes,279': u'Hernaes,279', u'New London Summary,1761.07.24.': u'New London Summary,1761.07.24.', u'VilaVilar,158': u'VilaVilar,158', u'Hernaes,251,253': u'Hernaes,251,253', u'Hernaes,272': u'Hernaes,272', u'Hernaes,256-258': u'Hernaes,256,258', u'Hernaes,270': u'Hernaes,270', u'Hernaes,271': u'Hernaes,271', u'Hernaes, 263-67': u'Hernaes,263-67', u'Hernaes,277': u'Hernaes,277', u'Hernaes,274': u'Hernaes,276', u'Hernaes,275': u'Hernaes,275', u'Vila Vilar, 250-51': u'Vila Vilar, 250-51', u'DailyNationalIntelligencer,1814.04.23.': u'DailyNationalIntelligencer,1814.04.23', u'Vila Vilar, 244-45': u'Vila Vilar, 244-45', u'Farias, 1946, 394': u'Farias, 1946, 394', u'VilaVilar,Cuadro4': u'VilaVilar,Cuadro4', u'Hernaes,276': u'Hernaes,276', u'Farias, 1986, 266': u'Farias, 1986, 266', u'Farias, 1986, 260': u'Farias, 1986, 260', u'Norregard,124-5,128-9': u'Norregard,124-5,128-9', u'Norregard,74': u'Norregard,74', u'AN,cod141,16:140': u'ANRJ,code141,16:140', u'Norregard,104,107': u'Norregard,104,107', u'Report of St. Bartholomew,06.04.19.': u'Report of St. Bartholomew,06.04.19.', u'Studnicki-Gizbert (2007), 60, 197n100': u'Studnicki-Gizbert (2007), 60, 197n100', u'Vila Vilar, 132': u'Vila Vilar, 132', u'Vila Vilar, 252-53': u'Vila Vilar, 252-53', u'Vila Vilar, 148-49n70': u'Vila Vilar, 148-49n70', u'Hernaes,282': u'Hernaes,282', u'London Chronicle, 1787.09.20.': u'London Chronicle, 1787.09.20.', u'Szymanski,67,76': u'Szymanski,67,76', u'Hernaes,281': u'Hernaes,281', u'Hernaes,280': u'Hernaes,280', u'LC,1788,06.24-26': u'LC,1788,06.24-26', u'Post Man,05.03.26.': u'Post Man,05.03.26', u"St.James's Evening  Chronicle, 64.11.17.": u"St.James's Evening  Chronicle, 64.11.17.", u'ANC Database, mfn 68066806-68116811(Regueyra, JBG/27 enero 1': u'ANC Database, mfn 68066806-68116811(Regueyra, JBG/27 enero 1', u'MMHGA,1796.09.06.': u'MMHGA,1796.09.06.', u'Hernaes,209': u'Hernaes,209', u'VilaVilar,149': u'VilaVilar,149', u'VilaVilar,Cuadro3, 262-63': u'VilaVilar,Cuadro3, 262-63', u'Hernaes,206': u'Hernaes,206', u'DailyCourant,28.04.11.': u'DailyCourant,28.04.11', u'Hernaes, 257,260': u'Hernaes, 257,258', u'Hernaes,276,288': u'Hernaes,276,288', u'Heywood Memorandum Book, Liverpool': u'LivRO,Heywood', u'Hernaes,186-88': u'Hernaes,186-88', u'Vila Vilar, 148-49n70, 173': u'Vila Vilar, 148-49n70, 173', u'NARA,RG36Savannahmanifests,box3,1795-96': u'NARA,Atlanta,RG36Savannahmanifests,box3,1795-', u'Santo Domingo, 55, Ramo 19, no 104, doc. 1, 1 Mar 1639.': u'AGI,Santo Domingo, 55, Ramo 19, no 104, doc. 1, 1 Mar 1639', u'Hernaes,366': u'Hernaes,366', u'"Memoire pour le Sieur Pierre Lesens"': u'Lessens', u'Hernaes,279,290': u'Hernaes,279,290', u'Acosta Saignes, 77': u'Acosta Saignes, 1967, 77', u'ANC Database, mfn 1247612476 (Regueyra, JBG / 18 a': u'ANC Database, mfn 1247612476 (Regueyra, JBG / 18 a', u"St.James'sChronicle,69.08.12.": u"St.James'sChronicle,69.08.12.", u'Farias, 1986, 272': u'Farias, 1986, 272', u'Daily Advertiser (London), 1776.07.22.': u'Daily Advertiser, 1776.07.22', u'Daily Post (London), 1720.04.29.': u'Daily Post, 1720.04.29', u'Daily Post (London), 1729.04.29.': u'Daily Post, 1729.04.29', u'VilaVilar,Cuadro2, 254-55': u'VilaVilar,Cuadro2, 254-55', u'Norregard,82,92': u'Norregard,82,92', u"Fog's,29.09.06.": u"Fog's,29.09.06", u'Bowser (1974), 49-50, 58-71, 365, 368-76': u'Bowser (1974), 49-50, 58-71, 365, 368-76"', u'GazetteerandNewDailyAdvertiser,1777.07.0': u'GazetteerandNewDailyAdvertiser,1777.07.0', u'1 Acton 240': u'Acton, 1:240', u'Hernaes,261-262': u'Hernaes,261-262'}

class Command(BaseCommand):
    vplaces = {}
    vregions = {}
    vbroad_regions = {}
    vparticular_outcomes = {}
    vresistance = {}
    vslaves_outcomes = {}
    vvessel_captured_outcomes = {}
    vowner_outcomes = {}
    vnationalities = {}
    vnationalities = {}
    vton_types = {}
    vrig_of_vessels = {}

    invalid_src_count = 0
    
    sources = {}
    def best_source(self, text_ref):
        """
        Finds the source based on the text ref by searching for the short ref that is the beginning of the text_ref
        """
        #if not text_ref:
        #    return None
        if len(text_ref) < 1:
            print("WARNING: No matching source")
            self.invalid_src_count += 1
            return None
        src = self.sources.get(text_ref, None)
        #srcs = filter(lambda src: short_ref_matches(src.short_ref, text_ref), self.sources)
        #if len(srcs) > 1:
        #    print("ERROR: More than one matching source for " + text_ref)
        #if len(srcs) > 0:
        #    return srcs[0]
        if src:
            return src
        else:
            return self.best_source(text_ref[:-1])

    option_list = BaseCommand.option_list + (
        make_option('--dry-run',
                    action='store_true',
                    dest='dry_run',
                    default=False,
                    help='Do not make any changes to the database but still look at the sources matching'),
        )
    args = '<>'
    help = 'Syncs the data from the legacy wilson database to the database configured in this project.'
    def handle(self, *args, **options):
        make_changes = True
        if options['dry_run']:
            make_changes = False
        unknown_port_value = 99801
        pag = Paginator(legacy_models.Voyages.objects.filter(suggestion=False, revision=1).order_by('voyageid'), 100)
        print "Paginator count %s" % pag.count
        print "Paginator page range count %s" % len(pag.page_range)
        print "Paginator last page number %s" % pag.page_range[-1]
        if make_changes:
            models.Voyage.objects.all().delete()
            models.VoyageShip.objects.all().delete()
            models.VoyageShipOwnerConnection.objects.all().delete()
            models.VoyageShipOwner.objects.all().delete()
            models.VoyageOutcome.objects.all().delete()
            models.VoyageDates.objects.all().delete()
            models.VoyageCaptain.objects.all().delete()
            models.VoyageCaptainConnection.objects.all().delete()
            models.VoyageSourcesConnection.objects.all().delete()
            models.VoyageItinerary.objects.all().delete()
            models.VoyageSlavesNumbers.objects.all().delete()
        self.sources = {x.short_ref.replace(' ', ''): x for x in list(models.VoyageSources.objects.all()) if x.short_ref}
        self.vplaces = {x.value: x for x in list(models.Place.objects.all())}
        self.vregions = {x.value: x for x in list(models.Region.objects.all())}
        self.vbroad_regions = {x.value: x for x in list(models.BroadRegion.objects.all())}
        self.vparticular_outcomes = {x.value: x for x in list(models.ParticularOutcome.objects.all())}
        self.vresistance = {x.value: x for x in list(models.Resistance.objects.all())}
        self.vslaves_outcomes = {x.value: x for x in list(models.SlavesOutcome.objects.all())}
        self.vvessel_captured_outcomes = {x.value: x for x in list(models.VesselCapturedOutcome.objects.all())}
        self.vowner_outcomes = {x.value: x for x in list(models.OwnerOutcome.objects.all())}
        self.vnationalities = {x.value: x for x in list(models.Nationality.objects.all())}
        self.vton_types = {x.value: x for x in list(models.TonType.objects.all())}
        self.vrig_of_vessels = {x.value: x for x in list(models.RigOfVessel.objects.all())}
        self.vvoyage_groupings = {x.value: x for x in list(models.VoyageGroupings.objects.all())}
        count = 0
        try:
            for x in pag.page_range:
                for i in pag.page(x).object_list:
                    voyageObj = models.Voyage()
                    count += 1
                    print count
                    if i.voyageid is not None:
                        voyageObj.voyage_id = i.voyageid
                        if make_changes:
                            voyageObj.save()
                    ship = models.VoyageShip()
                    #ship.voyage = voyageObj
                    # There are some null values in wilson that should be false instead
                    voyageObj.voyage_in_cd_rom = not not i.evgreen
                    if i.xmimpflag:
                        xmimpflag = int(i.xmimpflag)
                        xmimpflagref = find_by_value(self.vvoyage_groupings, xmimpflag)
                        #xmimpflags = filter(lambda x: x.value == xmimpflag, self.vvoyage_groupings)
                        #xmimpflags = models.VoyageGroupings.objects.filter(value=xmimpflag)
                        #if i.xmimpflag and len(xmimpflags) >= 1:
                        #    voyageObj.voyage_groupings = xmimpflags[0]
                        if xmimpflagref:
                            voyageObj.voyage_groupings = xmimpflagref
                        #if i.xmimpflag and len(xmimpflags) < 1:
                        elif i.xmimpflag and not xmimpflagref:
                            print "ERROR: xmimpflag has invalid VoyageGroupings value: %s" % xmimpflag
                    if i.shipname:
                        ship.ship_name = i.shipname
                    if i.national:
                        ship.nationality_ship = find_by_value(self.vnationalities, i.national)
                    ship.tonnage = i.tonnage
                    if i.tontype:
                        ship.ton_type = find_by_value(self.vton_types, i.tontype)
                    if i.rig:
                        ship.rig_of_vessel = find_by_value(self.vrig_of_vessels, i.rig.id)
                    ship.guns_mounted = i.guns
                    ship.year_of_construction = i.yrcons
                    if i.placcons:
                        ship.vessel_construction_place = find_by_value(self.vplaces, i.placcons.id)
                    if i.constreg:
                        ship.vessel_constructoin_region = find_by_value(self.vregions, i.constreg)
                    ship.year_of_construction = i.yrcons
                    ship.registered_year = i.yrreg
                    if i.placreg:
                        ship.registered_place = find_by_value(self.vplaces, i.placreg)
                    if i.regisreg:
                        ship.registered_region = find_by_value(self.vregions, i.regisreg)
                    if i.natinimp:
                        ship.imputed_nationality = models.Nationality.objects.get(value=i.natinimp)
                    if i.tonmod:
                        ship.tonnage_mod = str(round(i.tonmod, 1))
                    #ship.save()
                    #voyageObj.voyage_ship = ship
                    #voyageObj.save()

                    # Owners section
                    letters = map(chr, range(97, 97 + 16)) # from a to p
                    for idx, letter in enumerate(letters):
                        # Inserting ownera, ownerb, ..., ownerp
                        attr = getattr(i, 'owner' + letter)
                        if attr:
                            if make_changes:
                                tmpOwner = models.VoyageShipOwner.objects.create(name=attr)
                                # Create voyage-owner connection
                                models.VoyageShipOwnerConnection.objects.create(owner=tmpOwner, voyage=voyageObj, owner_order=(idx+1))
                    outcome = models.VoyageOutcome()
                    #outcome.voyage = voyageObj
                    if i.fate:
                        outcome.particular_outcome = find_by_value(self.vparticular_outcomes, i.fate.id)
                    if i.resistance:
                        outcome.resistance = find_by_value(self.vresistance, i.resistance.id)
                    if i.fate2:
                        outcome.outcome_slaves = find_by_value(self.vslaves_outcomes, i.fate2.id)
                    if i.fate3:
                        outcome.vessel_captured_outcome = find_by_value(self.vvessel_captured_outcomes, i.fate3.id)
                    if i.fate4:
                        outcome.outcome_owner = find_by_value(self.vowner_outcomes, i.fate4.id)
                    #outcome.save()

                    itinerary = models.VoyageItinerary()
                    #itinerary.voyage = voyageObj
                    if i.portdep:
                        itinerary.port_of_departure = find_by_value(self.vplaces, i.portdep.id)
                    if i.embport:
                        itinerary.int_first_port_emb = find_by_value(self.vplaces, i.embport.id)
                    if i.embport2:
                        itinerary.int_second_port_emb = find_by_value(self.vplaces, i.embport2.id)
                    if i.embreg:
                        itinerary.int_first_region_purchase_slaves = find_by_value(self.vregions, i.embreg)
                    if i.embreg2:
                        itinerary.int_second_region_purchase_slaves = find_by_value(self.vregions, i.embreg2)
                    if i.arrport:
                        itinerary.int_first_port_dis = find_by_value(self.vplaces, i.arrport.id)
                    if i.arrport2:
                        itinerary.int_second_port_dis = find_by_value(self.vplaces, i.arrport2.id)
                    if i.regarr:
                        itinerary.int_first_region_slave_landing = find_by_value(self.vregions, i.regarr)
                    if i.regarr2:
                        itinerary.int_second_region_slave_landing = find_by_value(self.vregions, i.regarr2)
                    itinerary.ports_called_buying_slaves = i.nppretra
                    if i.plac1tra:
                        itinerary.first_place_slave_purchase = find_by_value(self.vplaces, i.plac1tra.id)
                    if i.plac2tra:
                        itinerary.second_place_slave_purchase = find_by_value(self.vplaces, i.plac2tra.id)
                    if i.plac3tra:
                        itinerary.third_place_slave_purchase = find_by_value(self.vplaces, i.plac3tra.id)
                    if i.regem1:
                        itinerary.first_region_slave_emb = find_by_value(self.vregions, i.regem1.id)
                    if i.regem2:
                        itinerary.second_region_slave_emb = find_by_value(self.vregions, i.regem2.id)
                    if i.regem3:
                        itinerary.third_region_slave_emb = find_by_value(self.vregions, i.regem3.id)
                    if i.npafttra:
                        npafttraref = self.vplaces.get(i.npafttra, self.vplaces[unknown_port_value])
                    #npafttras = filter(lambda x: x.value == i.npafttra, self.vplaces)
                    #npafttras = models.Place.objects.filter(value=i.npafttra)
                    #if i.npafttra and len(npafttras) >= 1:
                    #    itinerary.port_of_call_before_atl_crossing = npafttras[0]
                    #if i.npafttra and len(npafttras) < 1:
                    #    print "WARNING: npafttra is invalid port value of %s, replacing value with '???' 99801" % i.npafttra
                    #    itinerary.port_of_call_before_atl_crossing = find_by_value(self.vplaces, unknown_port_value)
                    itinerary.number_of_ports_of_call = i.npprior
                    if i.sla1port:
                        itinerary.first_landing_place = find_by_value(self.vplaces, i.sla1port.id)
                    if i.adpsale1:
                        itinerary.second_landing_place = find_by_value(self.vplaces, i.adpsale1.id)
                    if i.adpsale2:
                        itinerary.third_landing_place = find_by_value(self.vplaces, i.adpsale2.id)
                    if i.regdis1:
                        itinerary.first_landing_region = find_by_value(self.vregions, i.regdis1.id)
                    if i.regdis2:
                        itinerary.second_landing_region = find_by_value(self.vregions, i.regdis2.id)
                    if i.regdis3:
                        itinerary.third_landing_region = find_by_value(self.vregions, i.regdis3.id)
                    if i.portret:
                        itinerary.place_voyage_ended = find_by_value(self.vplaces, i.portret.id)
                    if i.retrnreg:
                        itinerary.region_of_return = find_by_value(self.vregions, i.retrnreg.id)
                    if i.retrnreg1:
                        itinerary.broad_region_of_return = find_by_value(self.vbroad_regions, i.retrnreg1)
                    # Imputed itinerary variables
                    if i.ptdepimp:
                        itinerary.imp_port_voyage_begin = find_by_value(self.vplaces, i.ptdepimp)
                    if i.deptregimp:
                        itinerary.imp_region_voyage_begin = find_by_value(self.vregions, i.deptregimp)
                    if i.deptregimp1:
                        itinerary.imp_broad_region_voyage_begin = find_by_value(self.vbroad_regions, i.deptregimp1)
                    if i.majbuypt:
                        itinerary.principal_place_of_slave_purchase = find_by_value(self.vplaces, i.majbuypt)
                    if i.mjbyptimp:
                        itinerary.imp_principal_place_of_slave_purchase = find_by_value(self.vplaces, i.mjbyptimp.id)
                    if i.majbyimp:
                        itinerary.imp_principal_region_of_slave_purchase = find_by_value(self.vregions, i.majbyimp.id)
                    if i.majbyimp1:
                        itinerary.imp_broad_region_of_slave_purchase = find_by_value(self.vbroad_regions, i.majbyimp1)
                    if i.majselpt:
                        itinerary.principal_port_of_slave_dis = find_by_value(self.vplaces, i.majselpt)
                    if i.mjslptimp:
                        itinerary.imp_principal_port_slave_dis = find_by_value(self.vplaces, i.mjslptimp)
                    if i.mjselimp:
                        itinerary.imp_principal_region_slave_dis = find_by_value(self.vregions, i.mjselimp.id)
                    if i.mjselimp1:
                        itinerary.imp_broad_region_slave_dis = find_by_value(self.vbroad_regions, i.mjselimp1)
                    #itinerary.save()
                    #voyageObj.voyage_itinerary = itinerary
                    #voyageObj.save()

                    def mk_date(day_value, month_value, year_value):
                        """
                        :param day_value:
                        :param month_value:
                        :param year_value:
                        :return "mm,dd, yyyy":
                        """
                        tmpStr = ""
                        if month_value:
                            tmpStr += str(month_value)
                        tmpStr += ","
                        if day_value:
                            tmpStr += str(day_value)
                        tmpStr += ","
                        if year_value:
                            tmpStr += str(year_value)
                        if tmpStr == ',,':
                            return None
                        return tmpStr
                    # Voyage dates
                    date_info = models.VoyageDates()
                    #date_info.voyage = voyageObj
                    date_info.voyage_began = mk_date(i.datedepa, i.datedepb, i.datedepc)
                    date_info.slave_purchase_began = mk_date(i.d1slatra, i.d1slatrb, i.d1slatrc)
                    date_info.vessel_left_port = mk_date(i.dlslatra, i.dlslatrb, i.dlslatrc)
                    date_info.first_dis_of_slaves = mk_date(i.datarr32, i.datarr33, i.datarr34)
                    date_info.arrival_at_second_place_landing = mk_date(i.datarr36, i.datarr37, i.datarr38)
                    date_info.departure_last_place_of_landing = mk_date(i.ddepam, i.ddepamb, i.ddepamc)
                    date_info.voyage_completed = mk_date(i.datarr43, i.datarr44, i.datarr45)
                    if i.yeardep:
                        date_info.imp_voyage_began = ",," + str(i.yeardep)
                    if i.yearaf:
                        date_info.imp_departed_africa = ",," + str(i.yearaf)
                    if i.yearam:
                        date_info.imp_arrival_at_port_of_dis = ",," + str(i.yearam)
                    date_info.imp_length_home_to_disembark = i.voy1imp
                    date_info.imp_length_leaving_africa_to_disembark = i.voy2imp
                    # dateleftafr is made of:
                    # day: dlslatra
                    # month: dlslatrb
                    # year: dlslatrc
                    # Maybe the dlslatr. variables should be used always instead of the dateleftafr
                    if i.dateleftafr:
                        tmp = i.dateleftafr
                        # MM,DD,YYYY
                        date_info.date_departed_africa = mk_date(tmp.day, tmp.month, tmp.year)
                    elif i.dlslatrc:
                        date_info.date_departed_africa = mk_date(i.dlslatra, i.dlslatrb, i.dlslatrc)
                    #date_info.save()
                    #voyageObj.voyage_dates = date_info
                    #voyageObj.save()

                    # Captain and Crew section
                    crew = models.VoyageCrew()
                    #crew.voyage = voyageObj
                    crew.crew_voyage_outset = i.crew1
                    crew.crew_departure_last_port = i.crew2
                    crew.crew_first_landing = i.crew3
                    crew.crew_return_begin = i.crew4
                    crew.crew_end_voyage = i.crew5
                    crew.unspecified_crew = i.crew
                    crew.crew_died_before_first_trade = i.saild1
                    crew.crew_died_while_ship_african = i.saild2
                    crew.crew_died_middle_passage = i.saild3
                    crew.crew_died_in_americas = i.saild4
                    crew.crew_died_on_return_voyage = i.saild5
                    crew.crew_died_complete_voyage = i.crewdied
                    crew.crew_deserted = i.ndesert
                    if i.captaina:
                        #TODO change to get_or_create
                        if make_changes:
                            first_captain = models.VoyageCaptain.objects.create(name=i.captaina)
                            models.VoyageCaptainConnection.objects.create(captain_order=1, captain=first_captain, voyage=voyageObj)
                    if i.captainb:
                        #TODO change to get_or_create
                        if make_changes:
                            second_captain = models.VoyageCaptain.objects.create(name=i.captainb)
                            models.VoyageCaptainConnection.objects.create(captain_order=2, captain=second_captain, voyage=voyageObj)
                    if i.captainc:
                        #TODO change to get_or_create
                        if make_changes:
                            third_captain = models.VoyageCaptain.objects.create(name=i.captainc)
                            models.VoyageCaptainConnection.objects.create(captain_order=3, captain=third_captain, voyage=voyageObj)
                    #crew.save()
                    #voyageObj.voyage_crew = crew
                    #voyageObj.save()

                    # Voyage numbers and characteristics
                    characteristics = models.VoyageSlavesNumbers()
                    #characteristics.voyage = voyageObj
                    characteristics.num_slaves_intended_first_port = i.slintend
                    characteristics.num_slaves_intended_second_port = i.slinten2
                    characteristics.num_slaves_carried_first_port = i.ncar13
                    characteristics.num_slaves_carried_second_port = i.ncar15
                    characteristics.num_slaves_carried_third_port = i.ncar17
                    characteristics.total_num_slaves_purchased = i.tslavesp
                    characteristics.total_num_slaves_dep_last_slaving_port = i.tslavesd
                    characteristics.total_num_slaves_arr_first_port_embark = i.slaarriv
                    characteristics.num_slaves_disembark_first_place = i.slas32
                    characteristics.num_slaves_disembark_second_place = i.slas36
                    characteristics.num_slaves_disembark_third_place = i.slas39
                    #Imputed variables
                    characteristics.imp_total_num_slaves_embarked = i.slaximp
                    characteristics.imp_total_num_slaves_disembarked = i.slamimp
                    if i.jamcaspr:
                        characteristics.imp_jamaican_cash_price = str(i.jamcaspr)
                    characteristics.imp_mortality_during_voyage = i.vymrtimp

                    characteristics.num_men_embark_first_port_purchase = i.men1
                    characteristics.num_women_embark_first_port_purchase = i.women1
                    characteristics.num_boy_embark_first_port_purchase = i.boy1
                    characteristics.num_girl_embark_first_port_purchase = i.girl1
                    characteristics.num_adult_embark_first_port_purchase = i.adult1
                    characteristics.num_child_embark_first_port_purchase = i.child1
                    characteristics.num_infant_embark_first_port_purchase = i.infant1
                    characteristics.num_males_embark_first_port_purchase = i.male1
                    characteristics.num_females_embark_first_port_purchase = i.female1

                    characteristics.num_men_died_middle_passage = i.men2
                    characteristics.num_women_died_middle_passage = i.women2
                    characteristics.num_boy_died_middle_passage = i.boy2
                    characteristics.num_girl_died_middle_passage = i.girl2
                    characteristics.num_adult_died_middle_passage = i.adult2
                    characteristics.num_child_died_middle_passage = i.child2
                    characteristics.num_infant_died_middle_passage = i.infant2
                    characteristics.num_males_died_middle_passage = i.male2
                    characteristics.num_females_died_middle_passage = i.female2

                    characteristics.num_men_disembark_first_landing = i.men3
                    characteristics.num_women_disembark_first_landing = i.women3
                    characteristics.num_boy_disembark_first_landing = i.boy3
                    characteristics.num_girl_disembark_first_landing = i.girl3
                    characteristics.num_adult_disembark_first_landing = i.adult3
                    characteristics.num_child_disembark_first_landing = i.child3
                    characteristics.num_infant_disembark_first_landing = i.infant3
                    characteristics.num_males_disembark_first_landing = i.male3
                    characteristics.num_females_disembark_first_landing = i.female3

                    characteristics.num_men_embark_second_port_purchase = i.men4
                    characteristics.num_women_embark_second_port_purchase = i.women4
                    characteristics.num_boy_embark_second_port_purchase = i.boy4
                    characteristics.num_girl_embark_second_port_purchase = i.girl4
                    characteristics.num_adult_embark_second_port_purchase = i.adult4
                    characteristics.num_child_embark_second_port_purchase = i.child4
                    characteristics.num_infant_embark_second_port_purchase = i.infant4
                    characteristics.num_males_embark_second_port_purchase = i.male4
                    characteristics.num_females_embark_second_port_purchase = i.female4

                    characteristics.num_men_embark_third_port_purchase = i.men5
                    characteristics.num_women_embark_third_port_purchase = i.women5
                    characteristics.num_boy_embark_third_port_purchase = i.boy5
                    characteristics.num_girl_embark_third_port_purchase = i.girl5
                    characteristics.num_adult_embark_third_port_purchase = i.adult5
                    characteristics.num_child_embark_third_port_purchase = i.child5
                    characteristics.num_infant_embark_third_port_purchase = i.infant5
                    characteristics.num_males_embark_third_port_purchase = i.male5
                    characteristics.num_females_embark_third_port_purchase = i.female5

                    characteristics.num_men_disembark_second_landing = i.men6
                    characteristics.num_women_embark_first_port_purchase = i.women6
                    characteristics.num_boy_embark_first_port_purchase = i.boy6
                    characteristics.num_girl_embark_first_port_purchase = i.girl6
                    characteristics.num_adult_embark_first_port_purchase = i.adult6
                    characteristics.num_child_embark_first_port_purchase = i.child6
                    characteristics.num_infant_embark_first_port_purchase = i.infant6
                    characteristics.num_males_embark_first_port_purchase = i.male6
                    characteristics.num_females_embark_first_port_purchase = i.female6

                    # imputed variables 7
                    characteristics.imp_num_men_total = i.men7
                    characteristics.imp_num_women_total = i.women7
                    characteristics.imp_num_boy_total = i.boy7
                    characteristics.imp_num_girl_total = i.girl7
                    characteristics.imp_num_adult_total = i.adult7
                    characteristics.imp_num_child_total = i.child7
                    characteristics.imp_num_males_total = i.male7
                    characteristics.imp_num_females_total = i.female7

                    characteristics.imp_total_num_slaves_embarked = i.slaximp
                    characteristics.imp_num_adult_embarked = i.adlt1imp
                    characteristics.imp_num_children_embarked = i.chil1imp
                    characteristics.imp_num_male_embarked = i.male1imp
                    characteristics.imp_num_female_embarked = i.feml1imp
                    characteristics.total_slaves_embarked_age_identified = i.slavema1
                    characteristics.total_slaves_embarked_gender_identified = i.slavemx1

                    characteristics.imp_adult_death_middle_passage = i.adlt2imp
                    characteristics.imp_child_death_middle_passage = i.chil2imp
                    characteristics.imp_male_death_middle_passage = i.male2imp
                    characteristics.imp_female_death_middle_passage = i.feml2imp
                    characteristics.imp_num_adult_landed = i.adlt3imp
                    characteristics.imp_num_child_landed = i.chil3imp
                    characteristics.imp_num_male_landed = i.male3imp
                    characteristics.imp_num_female_landed = i.feml3imp
                    characteristics.total_slaves_landed_age_identified = i.slavema3
                    characteristics.total_slaves_landed_gender_identified = i.slavemx3
                    characteristics.total_slaves_dept_or_arr_age_identified = i.slavema7
                    characteristics.total_slaves_dept_or_arr_gender_identified = i.slavemx7
                    characteristics.imp_slaves_embarked_for_mortality = i.tslmtimp

                    characteristics.imp_mortality_ratio = i.vymrtrat

                    characteristics.percentage_men = i.menrat7
                    characteristics.percentage_women = i.womrat7
                    characteristics.percentage_boy = i.boyrat7
                    characteristics.percentage_girl = i.girlrat7
                    characteristics.percentage_male = i.malrat7
                    characteristics.percentage_child = i.chilrat7
                    if i.chilrat7:
                        characteristics.percentage_adult = 1 - i.chilrat7
                    if i.malrat7:
                        characteristics.percentage_female = 1 - i.malrat7

                    #characteristics.save()
                    #voyageObj.voyage_slaves_numbers = characteristics
                    #voyageObj.save()

                    if make_changes:
                        voyageObj.save()
                    
                        ship.voyage = voyageObj
                        outcome.voyage = voyageObj
                        itinerary.voyage = voyageObj
                        date_info.voyage = voyageObj
                        crew.voyage = voyageObj
                        characteristics.voyage = voyageObj
                    
                        ship.save()
                        outcome.save()
                        itinerary.save()
                        date_info.save()
                        crew.save()
                        characteristics.save()

                        voyageObj.voyage_ship = ship
                        # voyageObj.voyage_outcome = outcome
                        voyageObj.voyage_itinerary = itinerary
                        voyageObj.voyage_dates = date_info
                        voyageObj.voyage_crew = crew
                        voyageObj.voyage_slaves_numbers = characteristics
                    
                        voyageObj.save()

                    def insertSource(fieldvalue, order):
                        if fieldvalue:
                            # get the corrected text_ref from the source_fix_dict if it is there
                            txt_ref = source_fix_dict.get(fieldvalue, source_fix_dict.get(unicode(fieldvalue), fieldvalue))
                            if not txt_ref:
                                print("INFO: Skipping insert of source " + fieldvalue)
                                return
                            # Remove spaces from text_ref for matching with short_ref
                            to_be_matched = txt_ref.replace(' ', '')
                            src = self.best_source(to_be_matched)
                            if src:
                                if make_changes:
                                    models.VoyageSourcesConnection.objects.create(source=src, source_order=order, text_ref=txt_ref, group=voyageObj)
                            else:
                                print("WARNING: Could not find source for " + unidecode.unidecode(fieldvalue) + " on order " + str(order) + " for voyage " + str(voyageObj.voyage_id))
                                if make_changes:
                                    models.VoyageSourcesConnection.objects.create(source_order=order, text_ref=fieldvalue, group=voyageObj)
                                pass
                    # Alphabetical letters between a and r
                    letters = map(chr, range(97, 97+18))
                    for idx, letter in enumerate(letters):
                        # Inserting sourcea, sourceb, ..., sourcer
                        insertSource(getattr(i, 'source' + letter), (idx + 1))
                    if make_changes:
                        voyageObj.save()
                    sys.stdout.flush()
            print("There is " + str(self.invalid_src_count) + " text_refs without a matching short_ref")
        except Exception as ex:
            traceback.print_exc()
