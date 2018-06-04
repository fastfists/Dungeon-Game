String[] SPRITE_FILES = {"Skeleton.png"}; //enter path to pic here
int cellWidth = 32;
int cellHeight = 32;
import java.util.Scanner;
PImage image;
ArrayList<Sprite> sprites = new ArrayList<Sprite>();

void setup() {
  background(255);
  for(String SPRITE_FILE : SPRITE_FILES){
    image = loadImage(SPRITE_FILE);
    surface.setSize(image.width, image.height);
    stroke(255, 0, 0);
    strokeWeight(1);
    rectMode(CORNERS);
    noFill();
    for (int y = 0; y < image.height; y += cellHeight) {
      for (int x = 0; x < image.width; x += cellWidth) {
        sprites.add(new Sprite(x, y));
      }
    }
    String name = SPRITE_FILE.split("\\.")[0];
    for (Sprite s : sprites) {
      s.minimize();
    }
     image(image, 0, 0);
    for (Sprite s : sprites) {
      s.display();
    }
    int i = 1;
    print(name + "_ref = {");
    for (Sprite s: sprites){
      print("\t" + i + " : ");
      println(s + ",");
      i++;
    }
    print("}");
    println("\n\n");
  }
}

void draw() {
  image(image, 0, 0);
  for (Sprite s : sprites) {
    s.display();
  }
  noLoop();
}

int index(int x, int y, PImage img) {
  return x + y * img.width;
}
