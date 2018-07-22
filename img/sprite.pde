class Sprite{
  int left, right, top, bottom;
  
  Sprite(int l, int r, int t, int b){
    left = l;
    right = r;
    top = t;
    bottom = b;
  }
  
  Sprite(int l, int t){
    left = l;
    top = t;
    right = left + cellWidth - 1;
    bottom = top + cellHeight - 1;
  }
  
  void minimize(){
    //LEFT
    int empty = Integer.valueOf(image.pixels[0]); // feel free to comment this out
    //int empty = 0;
    for(int i = left; i <= right; i++){
      boolean blank = true;
      for(int j = top; j < bottom; j++){
        if(Integer.valueOf(image.pixels[index(i,j, image)]) != 0 || Integer.valueOf(image.pixels[index(i,j, image)]) != empty) {
          blank = false;
        }
      }
      if(!blank){
        left = i;
        break;
      }
    }
    
    //RIGHT
    for(int i = right; i >= left; i--){
      boolean blank = true;
      for(int j = top; j < bottom; j++){
        if(Integer.valueOf(image.pixels[index(i,j, image)]) != 0 || Integer.valueOf(image.pixels[index(i,j, image)]) != empty) {
          blank = false;
        }
      }
      if(!blank){
        right = i;
        break;
      }
    }
    
    //TOP
    for(int i = top; i <= bottom; i++){
      boolean blank = true;
      for(int j = left; j < right; j++){
        if(Integer.valueOf(image.pixels[index(j,i, image)]) != 0 || Integer.valueOf(image.pixels[index(j,i, image)]) != empty) {
          blank = false;
        }
      }
      if(!blank){
        top = i;
        break;
      }
    }
    
    //BOTTOM
    for(int i = bottom ; i >= top; i--){
      boolean blank = true;
      for(int j = left; j < right; j++){
        if(Integer.valueOf(image.pixels[index(j,i, image)]) != 0 || Integer.valueOf(image.pixels[index(j,i, image)]) != empty) {
          blank = false;
        }

      }
      if(!blank){
        bottom = i;
        break;
      }
    }
  }
  
  String toString(){
    String arg1 = "(" + left;
    String arg2 = ", " + top;
    String arg3 = ", " + (right - left);
    String arg4 = ", " + (bottom - top) + ")";
    return arg1 + arg2 + arg3 + arg4;
    
  }
  
  void display(){
    rect(left, top, right, bottom);
  }
}
