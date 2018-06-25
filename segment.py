""" Segment Module for Processing PDF Documents 
2018(c), Andrew Ferlitsch
"""

class Segment(object):
    """ Segment text into Regions """
    
    HEADING     = 1
    PARAGRAPH   = 2
    PAGENO      = 3
    COPYRIGHT   = 4
    
    def __init__(self, text):
        """ """
        self._text = text
        self._segments = []
        # Do Segmentation of the text
        self._segmentation()
        
    def _segmentation(self):
        """ Split text into paragraphs """
        para = ''
        
        # Split the text into lines
        lines = self._text.split('\n')
        # Process each line
        for line in lines:
            s_line = line.strip()
            # Blank Line: look for paragraph
            if s_line == '':
                if para != '':
                    self._segments.append( { 'text': para, 'tag': self.PARAGRAPH } )
                    para = ''
            # All Upper: Heading
            elif s_line.isupper():
                if para != '':
                    self._segments.append( { 'text': para, 'tag': self.PARAGRAPH } )
                    para = '' 
                self._segments.append( { 'text': line, 'tag': self.HEADING } )
            # Copyright
            elif s_line.lower().startswith("copyright"):
                if para != '':
                    self._segments.append( { 'text': para, 'tag': self.PARAGRAPH } )
                    para = '' 
                self._segments.append( { 'text': line, 'tag': self.COPYRIGHT } )
            else:
                # Look for page number
                pageno = False
                toks = s_line.split(' ')
                if len(toks) == 2:
                    if toks[0].lower() == 'page' and toks[1].isdigit():
                        pageno = True
                if not pageno:
                    # Look for heading
                    heading = True
                    for tok in toks:
                        if tok[0].isdigit() or tok[0].isupper() or tok[0] == '.':
                            pass
                        else:
                            heading = False
                else:
                    heading = False
                    
                if heading:
                    if para != '':
                        self._segments.append( { 'text': para, 'tag': self.PARAGRAPH } )
                        para = '' 
                    self._segments.append( { 'text': line, 'tag': self.HEADING } )
                elif pageno:      
                    if para != '':
                        self._segments.append( { 'text': para, 'tag': self.PARAGRAPH } )
                        para = '' 
                    self._segments.append( { 'text': line, 'tag': self.PAGENO } )  
                else:
                    if para != '':
                        para += '\n' + line
                    else:
                        para = line
                
        if para != '':
            self._segments.append( { 'text': para, 'tag': self.PARAGRAPH } )
            para = ''
            
    @property
    def segments(self):
        """ Getter for segments """
        return self._segments