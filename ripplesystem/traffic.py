import urllib, json, copy

filename = ['mon-4-1-2016', 'tues-5-1-2016', 'wed-6-1-2016', 'thurs-7-1-2016', 'fri-8-1-2016', 'sat-9-1-2016', 'sun-10-1-2016', 'mon-11-1-2016',
           'mon-1-2-2016', 'tues-2-2-2016', 'wed-3-2-2016', 'thurs-4-2-2016', 'fri-5-2-2016', 'sat-6-2-2016', 'sun-7-2-2016', 'mon-8-2-2016']

links = ['https://raw.githubusercontent.com/huseinzol05/Data-Visualization-Collection/master/traffic/weekone_json/summarized_mon.json',
        'https://raw.githubusercontent.com/huseinzol05/Data-Visualization-Collection/master/traffic/weekone_json/summarized_tue.json',
        'https://raw.githubusercontent.com/huseinzol05/Data-Visualization-Collection/master/traffic/weekone_json/summarized_wed.json',
        'https://raw.githubusercontent.com/huseinzol05/Data-Visualization-Collection/master/traffic/weekone_json/summarized_thur.json',
        'https://raw.githubusercontent.com/huseinzol05/Data-Visualization-Collection/master/traffic/weekone_json/summarized_fri.json',
        'https://raw.githubusercontent.com/huseinzol05/Data-Visualization-Collection/master/traffic/weekone_json/summarized_sat.json',
        'https://raw.githubusercontent.com/huseinzol05/Data-Visualization-Collection/master/traffic/weekone_json/summarized_sun.json',
        'https://raw.githubusercontent.com/huseinzol05/Data-Visualization-Collection/master/traffic/weekone_json/summary_week_2016-01-11.json',
        'https://raw.githubusercontent.com/huseinzol05/Data-Visualization-Collection/master/traffic/weektwo_json/summarized_mon.json',
        'https://raw.githubusercontent.com/huseinzol05/Data-Visualization-Collection/master/traffic/weektwo_json/summarized_tue.json',
        'https://raw.githubusercontent.com/huseinzol05/Data-Visualization-Collection/master/traffic/weektwo_json/summarized_wed.json',
        'https://raw.githubusercontent.com/huseinzol05/Data-Visualization-Collection/master/traffic/weektwo_json/summarized_thur.json',
        'https://raw.githubusercontent.com/huseinzol05/Data-Visualization-Collection/master/traffic/weektwo_json/summarized_fri.json',
        'https://raw.githubusercontent.com/huseinzol05/Data-Visualization-Collection/master/traffic/weektwo_json/summarized_sat.json',
        'https://raw.githubusercontent.com/huseinzol05/Data-Visualization-Collection/master/traffic/weektwo_json/summarized_sun.json',
        'https://raw.githubusercontent.com/huseinzol05/Data-Visualization-Collection/master/traffic/weektwo_json/summary_week_2016-02-08.json']

print "downloading.."
response = urllib.urlopen('https://raw.githubusercontent.com/huseinzol05/Data-Visualization-Collection/master/traffic/kl_segments.geojson')
master_geojson = json.loads(response.read())

for n, i in enumerate(links):
    
    print "current: " + str(n)
    geojson = copy.copy(master_geojson)
    
    response = urllib.urlopen(i)
    traffic_json = json.loads(response.read())
    
    for x in xrange(len(geojson['features'])):
        
        found = False
        for z in traffic_json:

            if int(geojson['features'][x]['properties']['segment_id']) == int(z):
                found = True
                
                traffic = {}
                traffic.update({'avg' : traffic_json[z]['day_avg']})
                for c in xrange(24):
                    
                    try:
                        traffic.update({str(c) : traffic_json[z]['hour_avg'][str(c)]})
                    except:
                        traffic.update({str(c) : 0})
                
                geojson['features'][x]['properties']['traffic'] = traffic
                
                color = {}
                for v in geojson['features'][x]['properties']['traffic']:
                    
                    if geojson['features'][x]['properties']['traffic'][v] >= 100:
                        color.update({v : '#CCB974'})
                    
                    elif geojson['features'][x]['properties']['traffic'][v] >= 80:
                        color.update({v : '#55A868'})
                    
                    elif geojson['features'][x]['properties']['traffic'][v] >= 60:
                        color.update({v : '#8172B2'})
                        
                    elif geojson['features'][x]['properties']['traffic'][v] >= 40:
                        color.update({v : '#64B5CD'})
                        
                    elif geojson['features'][x]['properties']['traffic'][v] >= 20:
                        color.update({v : '#4C72B0'})
                        
                    elif geojson['features'][x]['properties']['traffic'][v] > 0:
                        color.update({v : '#C44E52'})
                        
                    else:
                        color.update({v : 'grey'})
                
                geojson['features'][x]['properties']['color'] = color
                break
                
        if not found:
            geojson['features'][x]['properties']['notfound'] = 1
            
    for x in reversed(xrange(len(geojson['features']))):
        
        try:
            if geojson['features'][x]['properties']['notfound'] == 1:
                del geojson['features'][x]
        except:
            continue
            
    with open(filename[n] + '.geojson', 'w') as fopen:
        json.dump(geojson, fopen)