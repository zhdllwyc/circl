
import argparse
import re


# Define macros
top_32_target = 320
cs1_target = 8380417
bottom_32_bound = 16384

def parse_file(fn):
    total_sig = -1
    count_y_upper = 0
    count_y_upper_lower = 0
    count_cs1= 0
    count_codition_met = 0
    
    start = 0
    hit_on_y = -1
    m_y_sig = {}
    m_y_sig["message"] = ""
    m_y_sig["y"] = ""
    m_y_sig["signature"] = ""
    m_y_sig["cs1"] = ""

    met={}
    file1 = open(fn, 'r')
    for line in file1:

        if("BenchmarkSign-16" in line):
            start = 1

        if((start==1) and ("m" in line)):
            total_sig = total_sig + 1
            m_y_sig["message"] = line

        if((start==1) and ("y" in line)):
            hit_on_y = -1
            line_space = re.sub("[^0-9]", repl= ' ', string=line.split("y")[1]).strip()
            m_y_sig["y"] = line_space
            split_line = line_space.split()
            try:
                assert len(split_line)==1024
            except AssertionError:
                print("y length is %d" % len(split_line) )
            for idx, x in enumerate(split_line):
                # y is 320 at this index
                if(int(x)==top_32_target):
                    count_y_upper = count_y_upper + 1
                    if((idx%2==0) and (int(split_line[idx+1]) < bottom_32_bound)):
                        count_y_upper_lower = count_y_upper_lower + 1
                        hit_on_y = idx

        if((start==1) and ("cs1" in line)):
            line_space = re.sub("[^0-9]", repl= ' ', string=line.split("cs1")[1]).strip()
            m_y_sig["cs1"] = line_space
            split_line = line_space.split()
            try:
                assert len(split_line)==1024
            except AssertionError:
                print("cs1 length is %d" % len(split_line) )
            for x in split_line:
                if(int(x)==cs1_target):
                    count_cs1 = count_cs1 + 1
            if(hit_on_y!=-1):
                if(int(split_line[hit_on_y]) != cs1_target):
                    hit_on_y = -1
                    print(m_y_sig)
                else:
                    count_codition_met = count_codition_met + 1
                    met[hit_on_y] = 1

        if((start==1) and ("sig.z" in line)):
            line_space = re.sub("[^0-9]", repl= ' ', string=line.split("sig.z")[1]).strip()
            m_y_sig["signature"] = line_space
            split_line = line_space.split()
            try:
                assert len(split_line)==1024
            except AssertionError:
                print("sig.z length is %d" % len(split_line) )
            if(hit_on_y!=-1):
                if(int(split_line[hit_on_y]) != top_32_target):
                    print("Wrong!!!!!!!")
                    print(total_sig)
                    print(m_y_sig)
                    print(int(split_line[hit_on_y]))
                    return
                else:
                    print("Condition met at index %d" % hit_on_y)
            

    print(total_sig)
    print("Total we collect %d number of entries in y as %d." % (count_y_upper, top_32_target))
    print("Total we collect %d number of (int32, int32) in y as (%d, <%d)." % (count_y_upper_lower, top_32_target, bottom_32_bound))
    print("Total we collect %d number of entries in cs1 as %d." % (count_cs1, cs1_target))
    print("Total we collect %d number of condition met for arbitrary position" % (count_codition_met))
    not_found = 0
    for i in range(0,1024,2):
        if(i not in met):
            not_found = not_found + 1
            print("index %d not found" % i)

    print("not found %d " % not_found)

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('file')

    
    args = parser.parse_args()
    file_name = args.file

    parse_file(file_name)


if __name__ == "__main__":
    main()