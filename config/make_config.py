import re

z_low = 30
z_up = 60
thresh = 1.E-11

class Nucl:
    def __init__(self,z,n,count):
        self.z = z
        self.n = n
        self.count = count

if __name__ == "__main__":
    ifile = open('abundance_987.txt','r')
    nuclides = []
    for line in ifile:
        words = list(filter(None, re.split('\s+', line)))
        if words[0].isdigit():
            z = int(words[1])
            n = int(words[0]) - z
            c = float(words[2])
            if z > z_low and z < z_up:
                if c > thresh:
                    nuclides.append(Nucl(z,n,int(c/thresh)))    
    
    ifile.close()

    ofile = open('abundance_987_all.yaml','w')
    total = 0
    print len(nuclides)
    for nucl in nuclides:
        ofile.write('    - InitZ: %u\n' % nucl.z)
        ofile.write('      InitN: %u\n' % nucl.n)
        ofile.write('      InitCounts: %u\n' % nucl.count)
        total = total + nucl.count

    ofile.close()
    print ("total number of trial = %u" % total)
        
