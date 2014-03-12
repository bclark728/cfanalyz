# parses campaign finance html into json file
#  copyright 2014, Bryan Clark, bryan.allan.clark@gmail.com

import pprint;
pp = pprint.PrettyPrinter(indent=1);

# turns raw html into nested list structure
def recursivesplit(content, L):
 if(len(L) == 0):
  return [];
 s = content;
 pieces = s.split(L[0]);
 values = [pieces[0]];
 for p in pieces[1:]:
  values.append(recursivesplit(p,L[1:]));
 return values;

def mineferbucks(L):
 if(type(L) is str):
  if('$' in L):
   return [L];
  else:
   return [];
 elif(type(L) is list):
   ret = [];
   for l in L:
    ret += mineferbucks(l);
   return ret;
 else:
  return [];

def dictify(L):
 candidates = L[1:];
 ret = {};
 for i in range(0,len(candidates)):
  name   = candidates[i][0];
  party  = candidates[i][1][0];
  office = candidates[i][1][1][0];
  ret[name] = {'party':  party,
               'office': office,
	       'donors': {}      };
  for j in candidates[i][1][1][1:]:
   for k in j[1:]:
    ret[name]['donors'][k[0]]={};
    for l in k[1:]:
     ret[name]['donors'][k[0]]['address']=l[0];
     ret[name]['donors'][k[0]]['donations']=mineferbucks(l[1:]);
     # NOTE: this is currently broken because it does not deal with
     #       balance entries.
 return ret;

##
# MAIN PROGRAM
##

import sys;
import json;

if(len(sys.argv) != 3):
 print("SYNTAX: python3 parse.py <input_file> <output_file>");
 exit(1);

input   = open(sys.argv[1], "r");
content = input.read();
content = ' '.join(content.split());
input.close();

#define splitters
cand_str = "<td class=\"body\"><b><span class=\"name\" style=\"\">";
prty_str = "</span><span class=\"partyname\">";
offc_str = "</span><span class=\"officename\">";
dnrs_str = "</span></b></td> </tr> <tr class=\"paged\"> <td class=\"body\"></td> </tr>";
name_str = "<tr class=\"paged\"> <td class=\"body\"> <div class=\"sub\"><span class=\"name\" style=\"\">";
addr_str = "</span><span class=\"address\">";
date_str = "</span><span class=\"purposecode\"></span><span class=\"date\">";
amnt_str = "</span><span class=\"money\">";
end_str  = "</span>";
splitters = [cand_str, prty_str, offc_str, dnrs_str, name_str, \
             addr_str, date_str, amnt_str, end_str];

#preprocess by cutting out header
content = cand_str.join(content.split(cand_str)[1:]);
content = cand_str + content;

#process into nested list structure
values = recursivesplit(content, splitters);

#postprocess into nested dictionary
data = dictify(values);

#dump as json package to output file

output = open(sys.argv[2], 'w');
json.dump(data, output);
output.close();
