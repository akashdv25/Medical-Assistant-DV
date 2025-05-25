## Ocr setup 

![img](/img/ocr.png)


`This includes the setup for the advanced ocr setup we will implement in the future for handwritten presriptions SOTA in its use case`



`Documentation link` : [Click here](https://paddlepaddle.github.io/PaddleOCR/main/en/quick_start.html) 

<br>


### Quick start

- **Installation for cpu** : ``python -m pip install paddlepaddle==3.0.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/``

<br>

- **Install paddleocr**: ``pip install paddleocr==3.0.0``
  
### Script

``from paddleocr import PaddleOCR``

ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False)

result = ocr.predict(
    input="image_path")


for res in result:
    print(res['rec_texts'])``
