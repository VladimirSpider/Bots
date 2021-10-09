import requests
from bs4 import BeautifulSoup as BS
import re
import math
cars = {"Audi" : "1900",
     "BMW" : "3500",
     "Mercedes-Benz" : "17200",
     "Opel" : "19000",
     "Volkswagen" : "25200"
    }
cars_model = {"Audi" : {
                        '2': '100',
                        '3': '200',
                        '5': '80',
                        '6': '90',
                        '25': 'A1',
                        '7': 'A2',
                        '8': 'A3',
                        '9': 'A4',
                        '33': 'A4 Allroad',
                        '31': 'A5',
                        '10': 'A6',
                        '12': 'A6 Allroad',
                        '34': 'A7',
                        '11': 'A8',
                        '13': 'Cabriolet',
                        '14': 'Coupé',
                        '50': 'e-tron',
                        '43': 'Q1',
                        '45': 'Q2',
                        '37': 'Q3',
                        '57': 'Q4',
                        '32': 'Q5',
                        '15': 'Q7',
                        '46': 'Q8',
                        '16': 'quattro',
                        '29': 'R8',
                        '26': 'RS2',
                        '36': 'RS3',
                        '27': 'RS4',
                        '17': 'RS5',
                        '28': 'RS6',
                        '40': 'RS7',
                        '41': 'RSQ3',
                        '55': 'RSQ8',
                        '42': 'S1',
                        '18': 'S2',
                        '19': 'S3',
                        '20': 'S4',
                        '30': 'S5',
                        '21': 'S6',
                        '38': 'S7',
                        '22': 'S8',
                        '47': 'SQ2',
                        '39': 'SQ5',
                        '44': 'SQ7',
                        '54': 'SQ8',
                        '-38': 'TT (alle)',
                        '23': 'TT',
                        '35': 'TT RS',
                        '4': 'TTS',
                        '24': 'V8'
                        },

    "BMW" : {
                '-20': 'серии 1',
                '73': '114',
                '2': '116',
                '3': '118',
                '4': '120',
                '59': '123',
                '61': '125',
                '328': '128',
                '5': '130',
                '58': '135',
                '87': '1er M Coupé',
                '71': '2002',
                '-55': 'серии 2',
                '110': '214 Active Tourer',
                '116': '214 Gran Tourer',
                '106': '216',
                '111': '216 Active Tourer',
                '114': '216 Gran Tourer',
                '90': '218',
                '107': '218 Active Tourer',
                '112': '218 Gran Tourer',
                '84': '220',
                '108': '220 Active Tourer',
                '113': '220 Gran Tourer',
                '91': '225',
                '109': '225 Active Tourer',
                '104': '228',
                '125': '230',
                '322': '2er Gran Coupé',
                '-21': 'серии 3',
                '7': '315',
                '8': '316',
                '9': '318',
                '75': '318 Gran Turismo',
                '10': '320',
                '76': '320 Gran Turismo',
                '11': '323',
                '12': '324',
                '13': '325',
                '88': '325 Gran Turismo',
                '14': '328',
                '77': '328 Gran Turismo',
                '15': '330',
                '103': '330 Gran Turismo',
                '56': '335',
                '78': '335 Gran Turismo',
                '118': '340',
                '130': '340 Gran Turismo',
                '72': 'ActiveHybrid 3',
                '-53': 'серии 4',
                '115': '418',
                '98': '418 Gran Coupé',
                '80': '420', '99': '420 Gran Coupé',
                '102': '425',
                '124': '425 Gran Coupé',
                '81': '428',
                '100': '428 Gran Coupé',
                '83': '430',
                '105': '430 Gran Coupé',
                '82': '435',
                '101': '435 Gran Coupé',
                '120': '440',
                '121': '440 Gran Coupé',
                '-22': 'серии 5',
                '16': '518',
                '17': '520',
                '74': '520 Gran Turismo',
                '18': '523',
                '19': '524',
                '20': '525',
                '21': '528',
                '22': '530',
                '65': '530 Gran Turismo',
                '23': '535',
                '66': '535 Gran Turismo',
                '24':'540',
                '25': '545',
                '26': '550',
                '67': '550 Gran Turismo',
                '70': 'ActiveHybrid 5',
                '-23': 'серии 6',
                '144': '620 Gran Turismo',
                '27': '628',
                '28': '630',
                '127': '630 Gran Turismo',
                '29': '633',
                '30': '635',
                '68': '640',
                '94': '640 GranCoupé',
                '128': '640 Gran Turismo',
                '31': '645',
                '32': '650',
                '95': '650 Gran Coupé',
                '-24': 'серии 7',
                '33': '725',
                '34': '728',
                '35': '730',
                '36': '732',
                '37': '735',
                '38': '740',
                '39': '745',
                '40': '750',
                '41': '760',
                '63': 'ActiveHybrid 7',
                '42': '840',
                '43': '850',
                '-26': 'серии X',
                '64': 'ActiveHybrid X6',
                '6': 'X1',
                '129': 'X2',
                '48': 'X3',
                '145': 'X3 M',
                '153': 'X3 M40',
                '92': 'X4',
                '146': 'X4 M',
                '119': 'X4 M40',
                '49': 'X5',
                '53': 'X5 M',
                '96': 'X5 M50',
                '60': 'X6',
                '62': 'X6 M',
                '97': 'X6 M50',
                '143': 'X7',
                '79': 'i3',
                '330': 'i4',
                '89': 'i8',
                '331': 'iX',
                '329': 'iX3',
                '-25': 'моделей M',
                '69': 'M135',
                '122': 'M140i',
                '117': 'M2',
                '85': 'M235',
                '123': 'M240i',
                '45': 'M3',
                '152': 'M340i',
                '93': 'M4',
                '46': 'M5',
                '86': 'M550',
                '47': 'M6',
                '126': 'M760',
                '154': 'M8',
                '140': 'M850',
                '-27': 'серии Z',
                '50': 'Z1',
                '51': 'Z3',
                '57': 'Z3 M',
                '52': 'Z4',
                '55': 'Z4 M',
                '54': 'Z8'
                },

    "Mercedes-Benz" : {
                        '126': '190',
                        '127': '200',
                        '128': '220',
                        '129': '230',
                        '130': '240',
                        '131': '250',
                        '132': '260',
                        '133': '270',
                        '134': '280',
                        '135': '290',
                        '136': '300',
                        '137': '320',
                        '138': '350',
                        '139': '380',
                        '140': '400',
                        '141': '416',
                        '142': '420',
                        '143': '450',
                        '144': '500',
                        '145': '560',
                        '146': '600',
                        '-4': 'A-Класс',
                        '2': 'A 140',
                        '3': 'A 150',
                        '4': 'A 160',
                        '5': 'A 170',
                        '6': 'A 180',
                        '7': 'A 190',
                        '8': 'A 200',
                        '9': 'A 210',
                        '221': 'A 220',
                        '220': 'A 250',
                        '298': 'A 35 AMG',
                        '229': 'A 45 AMG',
                        '-64': 'GT-Класс',
                        '242': 'AMG GT',
                        '282': 'AMG GT C',
                        '281': 'AMG GT R',
                        '247': 'AMG GT S',
                        '-5': 'B-Класс',
                        '12': 'B 150',
                        '11': 'B 160',
                        '13': 'B 170',
                        '14': 'B 180',
                        '15': 'B 200',
                        '222': 'B220',
                        '223': 'B 250',
                        '241': 'B Electric Drive',
                        '-6': 'C-Класс',
                        '16': 'C 160',
                        '17': 'C 180',
                        '18': 'C 200',
                        '19': 'C 220',
                        '20': 'C 230',
                        '21': 'C 240',
                        '22': 'C 250',
                        '23': 'C 270',
                        '24': 'C 280',
                        '44': 'C 300',
                        '25': 'C 30 AMG',
                        '27': 'C 320',
                        '26': 'C 32 AMG',
                        '28': 'C 350',
                        '29': 'C 36 AMG',
                        '245': 'C 400',
                        '30': 'C 43 AMG',
                        '246': 'C 450 AMG',
                        '31': 'C 55 AMG',
                        '198': 'C 63 AMG',
                        '-7': 'CE-Класс',
                        '32': 'CE 200',
                        '167': 'CE 220',
                        '216': 'CE 230',
                        '217': 'CE280',
                        '33': 'CE 300',
                        '234': 'CE 320',
                        '224': 'Citan',
                        '-8': 'CL-Класс',
                        '210': 'CL 160',
                        '35': 'CL 180',
                        '36': 'CL 200',
                        '37': 'CL 220',
                        '38': 'CL 230',
                        '211': 'CL 320',
                        '39': 'CL 420',
                        '40': 'CL 500',
                        '41': 'CL 55 AMG',
                        '42': 'CL 600',
                        '197': 'CL 63 AMG',
                        '43': 'CL 65 AMG',
                        '-45': 'CLA-Класс',
                        '225': 'CLA 180',
                        '255': 'CLA 180 Shooting Brake',
                        '226': 'CLA 200',
                        '256': 'CLA 200 Shooting Brake',
                        '227': 'CLA 220',
                        '257': 'CLA 220 Shooting Brake',
                        '228': 'CLA 250',
                        '258': 'CLA 250 Shooting Brake',
                        '326': 'CLA 35 AMG',
                        '230': 'CLA 45 AMG',
                        '259': 'CLA 45 AMG Shooting Brake',
                        '248': 'CLA Shooting Brake',
                        '-30': 'CLC-Класс',
                        '46': 'CLC 160',
                        '200': 'CLC 180',
                        '201': 'CLC 200',
                        '202': 'CLC 220',
                        '203': 'CLC 230',
                        '107': 'CLC 250',
                        '204': 'CLC 350',
                        '-9': 'CLK-Класс',
                        '168': 'CLK 200',
                        '169': 'CLK 220',
                        '186': 'CLK 230',
                        '187': 'CLK 240',
                        '188': 'CLK 270',
                        '170': 'CLK 280',
                        '171': 'CLK 320',
                        '172': 'CLK 350',
                        '173': 'CLK 430',
                        '174': 'CLK 500',
                        '45': 'CLK 55 AMG',
                        '189': 'CLK 63 AMG',
                        '-10': 'CLS-Класс',
                        '240': 'CLS 220',
                        '260': 'CLS 220 Shooting Brake',
                        '212': 'CLS 250',
                        '261': 'CLS 250 Shooting Brake',
                        '205': 'CLS 280',
                        '117': 'CLS 300',
                        '147': 'CLS 320',
                        '148': 'CLS 350',
                        '262': 'CLS 350 Shooting Brake',
                        '239': 'CLS 400',
                        '263': 'CLS 400 Shooting Brake',
                        '289': 'CLS 450',
                        '149': 'CLS 500',
                        '264': 'CLS 500 Shooting Brake',
                        '297': 'CLS 53 AMG',
                        '150': 'CLS 55 AMG',
                        '176': 'CLS 63 AMG',
                        '265': 'CLS 63 AMG Shooting Brake',
                        '249': 'CLS Shooting Brake',
                        '-11': 'E-Класс',
                        '47': 'E 200',
                        '48': 'E 220',
                        '49': 'E 230',
                        '50': 'E 240',
                        '51': 'E 250',
                        '52': 'E 260',
                        '53': 'E 270',
                        '54': 'E 280',
                        '55': 'E 290',
                        '56': 'E 300',
                        '57': 'E320',
                        '58': 'E 350',
                        '59': 'E 36 AMG',
                        '60': 'E 400',
                        '61': 'E 420',
                        '62': 'E 430',
                        '272': 'E 43 AMG',
                        '321': 'E 450',
                        '177': 'E 50',
                        '64': 'E 500',
                        '296': 'E 53 AMG',
                        '178': 'E 55 AMG',
                        '66': 'E 60 AMG',
                        '179': 'E 63 AMG',
                        '346': 'EQA',
                        '322': 'EQC',
                        '344': 'EQV',
                        '-12': 'G-Класс',
                        '152': 'G 230',
                        '151': 'G 240',
                        '153': 'G 250',
                        '154': 'G 270',
                        '155': 'G 280',
                        '156': 'G 290',
                        '157': 'G 300',
                        '158': 'G 320',
                        '160': 'G 350',
                        '159': 'G 400',
                        '161': 'G 500',
                        '68': 'G 55 AMG',
                        '218': 'G 63 AMG',
                        '219': 'G 65 AMG',
                        '-13': 'GL-Класс',
                        '180': 'GL 320',
                        '166': 'GL 350',
                        '244': 'GL 400',
                        '181': 'GL 420',
                        '182': 'GL 450',
                        '183': 'GL 500',
                        '196': 'GL 55 AMG',
                        '195': 'GL 63 AMG',
                        '-54': 'GLA-Класс',
                        '238': 'GLA 180',
                        '231': 'GLA 200',
                        '232': 'GLA 220',
                        '233': 'GLA 250',
                        '343': 'GLA 35 AMG',
                        '236': 'GLA 45 AMG',
                        '-66': 'GLB-Класс',
                        '335': 'GLB 180',
                        '328': 'GLB 200',
                        '336': 'GLB 220',
                        '329': 'GLB 250',
                        '339': 'GLB 35 AMG',
                        '-59': 'GLC-Класс',
                        '325': 'GLC 200',
                        '253': 'GLC 220',
                        '254': 'GLC 250',
                        '284': 'GLC 300',
                        '278': 'GLC 350',
                        '334': 'GLC 400',
                        '279': 'GLC 43 AMG',
                        '283': 'GLC 63 AMG',
                        '-58': 'GLE-Класс',
                        '266': 'GLE 250',
                        '324': 'GLE 300',
                        '251': 'GLE 350',
                        '252':'GLE 400',
                        '280': 'GLE 43 AMG',
                        '243': 'GLE 450',
                        '267': 'GLE 500',
                        '337': 'GLE 53 AMG',
                        '341': 'GLE 580',
                        '250': 'GLE 63 AMG',
                        '-31': 'GLK-Класс',
                        '175': 'GLK 200',
                        '206': 'GLK 220',
                        '63': 'GLK 250',
                        '207': 'GLK 280',
                        '65': 'GLK 300',
                        '208': 'GLK 320',
                        '209': 'GLK 350',
                        '-60': 'GLS-Класс',
                        '268': 'GLS 350',
                        '269': 'GLS 400',
                        '340': 'GLS 450',
                        '270': 'GLS 500',
                        '338': 'GLS 580',
                        '342': 'GLS 600',
                        '271': 'GLS 63',
                        '70': 'MB 100',
                        '-14': 'ML-Класс',
                        '71': 'ML 230',
                        '215': 'ML 250',
                        '72': 'ML 270',
                        '73': 'ML 280',
                        '67': 'ML 300',
                        '74': 'ML 320',
                        '75': 'ML 350',
                        '76': 'ML 400',
                        '192': 'ML 420',
                        '77': 'ML 430',
                        '69': 'ML 450',
                        '78': 'ML 500',
                        '79': 'ML 55 AMG',
                        '162': 'ML 63 AMG',
                        '-15': 'R-Класс',
                        '190': 'R 280',
                        '92': 'R 300',
                        '80': 'R 320',
                        '81': 'R 350',
                        '82': 'R 500',
                        '184': 'R 63 AMG',
                        '-16': 'S-Класс',
                        '213': 'S 250',
                        '185': 'S 260',
                        '83': 'S 280',
                        '84': 'S 300',
                        '85': 'S 320',
                        '86': 'S 350',
                        '87': 'S 400',
                        '88': 'S 420',
                        '89': 'S 430',
                        '191': 'S 450',
                        '90': 'S 500',
                        '91': 'S 55',
                        '193': 'S 550',
                        '285': 'S 560',
                        '93': 'S 600',
                        '194': 'S 63 AMG',
                        '294': 'S 650',
                        '94': 'S 65 AMG',
                        '-17': 'SL-Класс',
                        '95': 'SL 280',
                        '96': 'SL 300',
                        '97': 'SL 320',
                        '98': 'SL350',
                        '99': 'SL 380',
                        '237': 'SL 400',
                        '100': 'SL 420',
                        '101': 'SL 450',
                        '102': 'SL 500',
                        '103': 'SL 55 AMG',
                        '104': 'SL 560',
                        '105': 'SL 600',
                        '163': 'SL 60 AMG',
                        '199': 'SL 63 AMG',
                        '106': 'SL 65 AMG',
                        '164': 'SL 70 AMG',
                        '165': 'SL73 AMG',
                        '-62': 'SLC-Класс',
                        '274': 'SLC 180',
                        '275': 'SLC 200',
                        '273': 'SLC 250',
                        '288': 'SLC 280',
                        '276': 'SLC 300',
                        '277': 'SLC 43 AMG',
                        '-18': 'SLK-Класс',
                        '108': 'SLK 200',
                        '109': 'SLK 230',
                        '214': 'SLK 250',
                        '110': 'SLK 280',
                        '10': 'SLK 300',
                        '112': 'SLK 320',
                        '111': 'SLK 32 AMG',
                        '113': 'SLK 350',
                        '114': 'SLK 55 AMG',
                        '115': 'SLR',
                        '34': 'SLS AMG',
                        '116': 'Sprinter',
                        '-19': 'V-Класс',
                        '118': 'V 200',
                        '119': 'V 220',
                        '120': 'V 230',
                        '235': 'V 250',
                        '121': 'V 280',
                        '323': 'V 300',
                        '122': 'Vaneo',
                        '123': 'Vario',
                        '124': 'Viano',
                        '125': 'Vito',
                        '-65': 'X-Класс',
                        '286': 'X 220',
                        '287': 'X 250',
                        '312': 'X 350'
                        },

      "Opel" : {
                '38': 'Adam',
                '2': 'Agila',
                '28': 'Ampera',
                '45': 'Ampera-e',
                '34': 'Antara',
                '3': 'Arena',
                '4': 'Ascona',
                '5': 'Astra',
                '6': 'Calibra',
                '7': 'Campo',
                '39': 'Cascada',
                '32': 'Cavalier',
                '8': 'Combo',
                '9': 'Commodore',
                '10': 'Corsa',
                '42': 'Crossland (X)',
                '11': 'Diplomat',
                '12': 'Frontera',
                '43': 'Grandland X',
                '13': 'GT',
                '35': 'Insignia',
                '40': 'Insignia CT',
                '14': 'Kadett',
                '41': 'Karl',
                '15': 'Manta',
                '16': 'Meriva',
                '37': 'Mokka',
                '44': 'MokkaX',
                '17': 'Monterey',
                '18': 'Monza',
                '19': 'Movano',
                '33': 'Nova',
                '20': 'Omega',
                '21': 'Pick Up Sportscap',
                '22': 'Rekord',
                '23': 'Senator',
                '24': 'Signum',
                '25': 'Sintra',
                '26': 'Speedster',
                '27': 'Tigra',
                '29': 'Vectra',
                '30': 'Vivaro',
                '31': 'Zafira',
                '46': 'Zafira Life',
                '36': 'Zafira Tourer'
                },

    "Volkswagen" : {
                    '2': '181',
                    '5': 'Amarok',
                    '64': 'Arteon',
                    '10': 'Beetle',
                    '6': 'Bora',
                    '7': 'Buggy',
                    '9': 'Caddy',
                    '19': 'CC',
                    '12': 'Corrado',
                    '3': 'Crafter',
                    '41': 'Eos',
                    '13': 'Fox',
                    '-29': 'Golf (alle)',
                    '14': 'Golf',
                    '55': 'Golf Plus',
                    '40': 'Golf Sportsvan',
                    '81': 'ID.3',
                    '82': 'ID.4',
                    '15': 'Iltis',
                    '16': 'Jetta',
                    '18': 'Karmann Ghia',
                    '20': 'LT',
                    '21': 'Lupo',
                    '24': 'New Beetle',
                    '-37': 'Passat (alle)',
                    '25': 'Passat',
                    '62': 'Passat Alltrack',
                    '4': 'Passat CC',
                    '63': 'Passat Variant',
                    '26': 'Phaeton',
                    '27': 'Polo',
                    '8': 'Routan',
                    '28': 'Santana',
                    '29': 'Scirocco',
                    '30': 'Sharan',
                    '42': 'T1',
                    '31': 'T2',
                    '-1': 'T3',
                    '44': 'T3 Caravelle',
                    '22': 'T3 Kombi',
                    '45': 'T3 Multivan',
                    '46': 'T3 другие',
                    '-2': 'T4',
                    '33': 'T4 California',
                    '47': 'T4 Caravelle',
                    '23': 'T4 Kombi',
                    '48': 'T4 Multivan',
                    '49': 'T4 другие',
                    '-3': 'T5',
                    '34': 'T5 California',
                    '50': 'T5 Caravelle',
                    '32': 'T5 Kombi',
                    '51': 'T5 Multivan',
                    '52': 'T5 Shuttle',
                    '61': 'T5 Transporter',
                    '53': 'T5 другие',
                    '-57': 'T6',
                    '58': 'T6 California',
                    '56': 'T6 Caravelle',
                    '57': 'T6 Kombi',
                    '43': 'T6 Multivan',
                    '60': 'T6 Transporter',
                    '59': 'T6 другие',
                    '35': 'Taro',
                    '75': 'T-Cross',
                    '54': 'Tiguan',
                    '66': 'Tiguan Allspace',
                    '36': 'Touareg',
                    '37': 'Touran',
                    '65': 'T-Roc',
                    '11': 'up!',
                    '39': 'Vento',
                    '38': 'XL1',
                    '17': 'жук'
                    }
}
name_c = ""
nc = "1"
nm = "1"
np = "1"
URL = "https://www.mobile.de/ru/%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D1%8C/"+name_c+"/vhc:car,pgn:"+np+",pgs:10,ms1:"+nc+"_"+nm+"_"
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36', 'accept': '*/*'}

def get_html(url, params=None):
    r = requests.get(url, headers = HEADERS, params = params)
    return r

def number_pages(name_c,nc, nm):
    np = "1"
    URL = "https://www.mobile.de/ru/%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D1%8C/"+name_c+"/vhc:car,pgn:"+np+",pgs:10,ms1:"+nc+"_"+nm+"_"
    html = get_html(URL)
    html = BS(html.content, 'html.parser')
    np = html.find('div', class_ = 'search-result-header g-col-12 js-search-result-header hidden-print')\
        .find('h1', class_ = 'h2 u-text-orange').get_text(strip=True)
    print(np)
    np = np.replace("\u00A0","")
    print(np)
    np = re.findall(r'\d+', np)
    np = int(np[0]) / 10
    np = math.ceil(np)
    print("All pages - ", np)
    return np

'''def f():
    name_c = ""
    nc = input("Введите марку:")
    if nc in cars.keys():
        name_c = nc.lower()
        print(name_c)
        nc = cars[nc]
        print(nc)
        name_c = name_c.lower()
    else:
        print("ERROR")
        pass
    URL = "https://www.mobile.de/ru/%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D1%8C/"+name_c+"/vhc:car,pgn:"+np+",pgs:10,ms1:"+nc+"_"+nm+"_"
    html = get_html(URL)
    if html.status_code == 200:
        html = BS(html.content, 'html.parser')
        text = html.find('div', class_='form-group').find_next_sibling('div').find('select', class_ = "form-control form-control--dropdown js-model-dropdown js-track-event")
        text = text.find_all('option')
        a = {}
        for el in text:
            b = el.get('value')
            c = el.get_text(strip=True)
            a[b]=c
            print(b)
            print(c)
    print(a)
    return a

f()'''

def parse():
    j = 0
    name_c = ""
    name_car = input("Введите марку:")
    if name_car in cars.keys():
        name_c = name_car.lower()
        print(name_c)
        nc = cars[name_car]
        print(nc)
        name_c = name_c.lower()
    else:
        print("ERROR")
        pass
    nm = input("Введите модель:")
    if nm in cars_model[name_car].values():
        for el in cars_model[name_car].keys():
            if nm == cars_model[name_car][el]:
                nm = el
                print(nm)
    else:
        print("ERROR")
        pass
    pages = number_pages(name_c ,nc, nm)
    for np in range (1, (pages + 1)):
        np = str(np)
        print("PAGE №", np)
        URL = "https://www.mobile.de/ru/%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D1%8C/"+name_c+"/vhc:car,pgn:"+np+",pgs:10,ms1:"+nc+"_"+nm+"_"
        HOST = 'https://www.mobile.de/ru/%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D1%8C/'+ name_c +'/vhc:car,ms1:'+ nc +'__'
        html = get_html(URL)
        if html.status_code == 200:
            print("Hi")
            html = BS(html.content, 'html.parser')
            list_our = html.find_all('article', class_='list-entry g-row eyecatcher')
            if len(list_our) != 0:
                for el in html.find_all('article', class_='list-entry g-row eyecatcher'):
                    j += 1
                    try:
                        title = el.find('div', class_='vehicle-text g-row') \
                            .find('h3', class_='vehicle-title g-col-12 u-text-nowrap').get_text(strip=True)
                        title = title.replace("Новое", "")
                    except:
                        title = "Error"
                    try:
                        description = el.find('div', class_='vehicle-text g-row') \
                            .find('div', class_ = "vehicle-techspecs hidden-s").get_text(strip=True)
                    except:
                        description = "Error"
                    try:
                        cost = el.find('div', class_='vehicle-text g-row') \
                            .find('div', class_ = "g-col-s-6 g-col-m-4 u-text-right") \
                            .find('p', class_ = "seller-currency u-text-bold").get_text(strip=True)
                    except:
                        cost = "Error"
                    try:
                        year = el.find('div', class_='vehicle-text g-row') \
                            .find('div', class_="vehicle-information g-col-s-6 g-col-m-8") \
                            .find('p', class_="u-text-bold").get_text(strip=True)
                    except:
                        year = "Error"
                    try:
                        link = el.find('div', class_='g-row js-ad-entry') \
                            .find('a', class_="vehicle-data track-event u-block js-track-event js-track-dealer-ratings").get('href')
                        link = re.findall(r'/pg.*', link)[0]
                    except:
                        link = "Error"

                    print("№", j, "\n")
                    print(title)
                    print(year)
                    print(description)
                    print(cost)
                    print(HOST+link)

            ##########################################################################
            list_our = html.find_all('article', class_='list-entry g-row')
            if len(list_our) != 0:
                for el in html.find_all('article', class_='list-entry g-row'):
                    j += 1
                    try:
                        title = el.find('div', class_='vehicle-text g-row') \
                            .find('h3', class_='vehicle-title g-col-12 u-text-nowrap').get_text(strip=True)
                        title = title.replace("Новое", "")
                    except:
                        title = "Error"
                    try:
                        description = el.find('div', class_='vehicle-text g-row') \
                            .find('div', class_ = "vehicle-techspecs hidden-s").get_text(strip=True)
                    except:
                        description = "Error"
                    try:
                        cost = el.find('div', class_='vehicle-text g-row') \
                            .find('div', class_ = "g-col-s-6 g-col-m-4 u-text-right") \
                            .find('p', class_ = "seller-currency u-text-bold").get_text(strip=True)
                    except:
                        cost = "Error"
                    try:
                        year = el.find('div', class_='vehicle-text g-row') \
                            .find('div', class_="vehicle-information g-col-s-6 g-col-m-8") \
                            .find('p', class_="u-text-bold").get_text(strip=True)
                    except:
                        year = "Error"
                    try:
                        link = el.find('div', class_='g-row js-ad-entry') \
                            .find('a', class_="vehicle-data track-event u-block js-track-event js-track-dealer-ratings").get('href')
                        link = re.findall(r'/pg.*', link)[0]
                    except:
                        link = "Error"

                    print("№", j, "\n")
                    print(title)
                    print(year)
                    print(description)
                    print(cost)
                    print(HOST+link)

        else:
            print('Error')

#parse()
#number_pages()

