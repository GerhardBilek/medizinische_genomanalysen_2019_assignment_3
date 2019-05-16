#! /usr/bin/env python3

import vcf
import httplib2
import json

__author__ = 'Gerhard Bilek'

##
##
## Aim of this assignment is to annotate the variants with various attributes
## We will use the API provided by "myvariant.info" - more information here: https://docs.myvariant.info
## NOTE NOTE! - check here for hg38 - https://myvariant.info/faq
## 1) Annotate the first 900 variants in the VCF file
## 2) Store the result in a data structure (not in a database)
## 3) Use the data structure to answer the questions
##
## 4) View the VCF in a browser
##

class Assignment3:
    
    def __init__(self):
        ## Check if pyvcf is installed
        print("PyVCF version: %s" % vcf.VERSION)
        
        ## Call annotate_vcf_file here
        self.vcf_path = "chr16.vcf"  # TODO

    @property
    def annotate_vcf_file(self):
        '''
        - Annotate the VCF file using the following example code (for 1 variant)
        - Iterate of the variants (use first 900)
        - Store the result in a data structure
        :return:
        '''    
        print("TODO")
                
        ##
        ## Example loop
        ##
        
        ## Build the connection
        h = httplib2.Http()
        headers = {'content-type': 'application/x-www-form-urlencoded'}
                
        params_pos = []  # List of variant positions
        with open(self.vcf_path) as my_vcf_fh:
            vcf_reader = vcf.Reader(my_vcf_fh)
            for counter, record in enumerate(vcf_reader):
                params_pos.append(record.CHROM + ":g." + str(record.POS) + record.REF + ">" + str(record.ALT[0]))
                
                if counter >= 899:
                    break
        
        ## Build the parameters using the list we just built
        params = 'ids=' + ",".join(params_pos) + '&hg38=true'

        #print("Params_Pos: ", params_pos)
        #print("Params: ", params)

        ## Perform annotation
        res, con = h.request('http://myvariant.info/v1/variant', 'POST', params, headers=headers)
        annotation_result = con.decode('utf-8')

        ## Generate json object
        jsonobject = json.loads(annotation_result)

        return(jsonobject)
    
    def get_list_of_genes(self, jsonobject):
        '''
        Print the name of genes in the annotation data set
        :return:
        '''
        for object in jsonobject:
            if 'cadd' in object:
                if 'genename' in object['cadd']['gene']:
                    print(object['cadd']['gene']['genename'])

        #for object in jsonobject:
        #    if 'dbsnp' in object:
        #        if 'genename' in object['dbsnp']['gene']:
        #           print(object['dbsnp']['gene']['genename'])

    def get_num_variants_modifier(self, jsonobject):
        '''
        Print the number of variants with putative_impact "MODIFIER"
        :return:
        '''

        '''
        for object in jsonobject:
            if 'cadd' in object:
                if 'putative_impact' in object['ann']:
                #if 'putative_impact' in object:
                    print("boom")
        '''
        counter = 0
        for object in jsonobject:
            if 'snpeff' in object:          # (???) snpeff , cadd
                key, value = "putative_impact", "MODIFIER"
                if key in object['snpeff']['ann'] and value == object['snpeff']['ann']['putative_impact']:
                    counter += 1
        return(counter)

    def get_num_variants_with_mutationtaster_annotation(self, jsonobject):
        '''
        Print the number of variants with a 'mutationtaster' annotation
        :return:
        '''
        counter = 0
        for object in jsonobject:
            if 'dbnsfp' in object:
                if 'mutationtaster' in object['dbnsfp']:
                    counter+=1
        return(counter)
        
    
    def get_num_variants_non_synonymous(self, jsonobject):
        '''
        Print the number of variants with 'consequence' 'NON_SYNONYMOUS'
        :return:
        '''

        counter = 0
        for object in jsonobject:
            if 'cadd' in object:
                key, value = "consequence", "NON_SYNONYMOUS"
                if key in object['cadd'] and value == object['cadd']['consequence']:    # value  muss bis zum Key definiert werden.
                    counter += 1
        return counter

    
    def view_vcf_in_browser(self):
        '''
        - Open a browser and go to https://vcf.iobio.io/
        - Upload the VCF file and investigate the details
        :return:
        '''

        ## Document the final URL here
        print("The vcf file has been compressed and indexed via iTabixIt.app. The two resulting files, the compressed file (gz) and the index file (gz.tbi) were uploaded to https://vcf.iobio.io/")
        print("Resutls: https://vcf.iobio.io/?species=Human&build=GRCh38")
    
    def print_summary(self):
        annoData = self.annotate_vcf_file   # Syntax? Warum ohne Klammern??
        #for object in annoData: print(object)    # json objects
        print()
        print("List of Genes:")             # 9
        self.get_list_of_genes(annoData)
        print()
        print("Num of Modifier: ", self.get_num_variants_modifier(annoData)) # 4
        print()
        print("Num of Mutationtaster: ", self.get_num_variants_with_mutationtaster_annotation(annoData)) #5
        print()
        print("Num of nonSynonymous: ", self.get_num_variants_non_synonymous(annoData))
        print()
        print(self.view_vcf_in_browser())
        print()

def main():
    print("Assignment 3")
    assignment3 = Assignment3()
    assignment3.print_summary()
    print("Done with assignment 3")
        
        
if __name__ == '__main__':
    main()
   
    



