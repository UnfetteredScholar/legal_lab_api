class TextBox:
    def __init__(self, boxes_per_row, search_text, total_rows=1, x_offset=0, y_offset=0, box_width=20, row_height=25, control_x=0.8):
        self.boxes_per_row = boxes_per_row
        self.total_rows = total_rows
        self.search_text = search_text
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.box_width = box_width
        self.row_height = row_height
        self.control_x = control_x
        # self.font_size = font_size
        self.total_boxes = boxes_per_row * total_rows
        
    
    def fill_field(self, page, input_text, ind=0, fs=12):
        input_clean = ' '.join(input_text.split())
        text_instances = page.search_for(self.search_text)
        rect = text_instances[ind]
        x0, y0, x1, y1 = rect

        x_start = x0 + self.x_offset
        y_start = (y0 + y1) / 2 + self.y_offset

        for i, letter in enumerate(input_clean):
                row = i // self.boxes_per_row  
                col = i % self.boxes_per_row 
                if row < self.total_rows:
                    if col == 0: 
                        x_start = x0 + self.x_offset 
                       

                    x = x_start + (col * self.box_width)
                    x_start += self.control_x
                    y = y_start + (row * self.row_height)
                    

                    page.insert_text((x, y), letter, fontsize=fs)
                





class PDFOptionField:
    def __init__(self,control_x=0, control_y=0):
        self.control_x = control_x
        self.control_y = control_y

    def fill_option(self, page, selected_option,ind=0,new_x=0, partner =True):
        if selected_option == "Dr" and partner:
            text_instances = page.search_for("Ms")
            self.control_x = -26
        else:
            text_instances = page.search_for(selected_option)
            
        # if new_x:
        #     self.control_x = new_x

        if selected_option == "Female" and partner:
            self.control_x = -45
        if selected_option == "Mr" and partner:
            self.control_x = 14
       
        if text_instances:
            rect = text_instances[ind]
            x0, y0, x1, y1 = rect

            if new_x:            
                x_checkbox = x0 - new_x
            else:  
                x_checkbox = x0 - self.control_x   
            y_checkbox = ((y0 + y1) / 2) + self.control_y 

            page.insert_text((x_checkbox, y_checkbox), "X", fontsize=14)
        # else:
        #     st.error(f"Could not find the option '{selected_option}' in the PDF.")





class PDFTextFinder:
    def __init__(self, search_text, max_chars_per_row=10, control_x=10, control_y=8, row_height=0, max_rows=1):
        self.search_text = search_text
        self.control_x = control_x
        self.control_y = control_y
        self.max_chars_per_row = max_chars_per_row
        self.row_height = row_height
        self.max_rows = max_rows
        self.total_space = self.max_chars_per_row * self.max_rows


    def fill_field(self, page, input_text, ind=0, fs=10):
        words = input_text.split()  
        text_instances = page.search_for(self.search_text)

        if text_instances:
            rect = text_instances[ind] 
            x0, y0, x1, y1 = rect
            
            new_x = x0 + self.control_x  
            current_y = y0 + self.control_y  
            
            current_row = 1  
            current_line = "" 
            rem_num = 0


            for word in words:
                test_line = current_line + word

                if len(test_line) <= self.max_chars_per_row:
                    current_line = test_line + ' '
                else:
                    space_remaining = self.max_chars_per_row - len(current_line)

                    if space_remaining > 0:
                        current_line += word[:space_remaining] + '-'
                        page.insert_text((new_x, current_y), current_line.strip(), fontsize=fs)
                        current_line = word[space_remaining:] + ' '
                    else:
                        page.insert_text((new_x, current_y), current_line.strip(), fontsize=fs)
                        current_line = word + ' '

                    current_row += 1
                    if current_row > self.max_rows:
                        return
                    current_y += self.row_height

            if current_line.strip():
                page.insert_text((new_x, current_y), current_line.strip(), fontsize=fs)





