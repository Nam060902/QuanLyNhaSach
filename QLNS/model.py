from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from QLNS import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin
from datetime import datetime


class UserRole(UserEnum):
    USER = 1
    ADMIN = 2
    Employee = 3


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(100), nullable=False, unique=True)
    book = relationship('Book', backref='category', lazy=True)

    def __str__(self):
        return self.name


book_tag = db.Table('book_tag',
                    Column('book_id', ForeignKey('book.id'), nullable=False, primary_key=True),
                    Column('tag_id', ForeignKey('tag.id'), nullable=False, primary_key=True))



class Book(BaseModel):
    __tablename__ = 'book'

    name = Column(String(100), nullable=False, unique=True)
    author = Column(String(50), nullable=False)
    description = Column(Text)
    price = Column(Float, default=0)
    image = Column(String(100))
    inventory = Column(Integer, default=0)
    active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    bill_details = relationship('BillDetails', backref='book', lazy=True)
    tags = relationship('Tag', secondary='book_tag', lazy='subquery',
                        backref=backref('book', lazy=True))
    comments = relationship('Comment', backref='book', lazy=True)
    goods_details = relationship('GoodsReceivedDetails', backref='book', lazy=True)


    def __str__(self):
        return self.name


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    phone = Column(String(10), nullable=True)
    avatar = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    bill = relationship('Bill', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name


class Bill(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    active = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, )
    details = relationship('BillDetails', backref='bill', lazy=True)


class BillDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    bill_id = Column(Integer, ForeignKey(Bill.id), nullable=False)


class GoodsReceived(BaseModel):
    sum_quantity = Column(Integer, nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    goods_details = relationship('GoodsReceivedDetails', backref='goodsReceived', lazy=True)


class GoodsReceivedDetails(BaseModel):
    name = Column(String(100), nullable=False)
    author = Column(String(50), nullable=False)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    goodsReceived_id = Column(Integer, ForeignKey(GoodsReceived.id), nullable=False)

class Comment(BaseModel):
    content = Column(String(255), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)

    def __str__(self):
        return self.content


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # db.drop_all()

        import hashlib
        password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        u = User(name='Nam', username='admin', password=password, phone='0378435023',
                 user_role=UserRole.ADMIN,
                 avatar='https://c.pxhere.com/images/0d/18/4fa31701d2cfa087836d807967f3-1447663.jpg!d')
        db.session.add(u)
        db.session.commit()

        password = str(hashlib.md5('123'.encode('utf-8')).hexdigest())
        u = User(name='Nhi', username='user', password=password, phone='0216494574',
                 user_role=UserRole.USER,
                 avatar='https://c.pxhere.com/images/0d/18/4fa31701d2cfa087836d807967f3-1447663.jpg!d')
        db.session.add(u)
        db.session.commit()

        c1 = Category(name='Khoa học công nghệ')
        c2 = Category(name='Nghệ thuật')
        c3 = Category(name='Truyện')
        c4 = Category(name='Tâm linh')
        c5 = Category(name='Tâm lý')

        db.session.add_all([c1, c2, c3, c4, c5])
        db.session.commit()

        p1 = Book(name='LIFE 3.0',
                  description='Nội dung chính của Life 3.0 bàn về Trí tuệ nhân tạo (Artificial Intelligence – AI)\
                                          và những ảnh hưởng của nó tới đời sống con người.',
                  author='Max Tegmark', price=161000, inventory=200, category_id=1,
                  image='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRwtSZBsv6e2Na_r8OE7FspJdou10qG6Qv8xQ&usqp=CAU')
        p2 = Book(name='Doraemon',
                  description='Đôrêmon là một chú mèo máy được Nôbitô, cháu ba đời của Nôbita gửi về quá khứ cho\
                                           ông mình để giúp đỡ Nôbita tiến bộ, tức là cũng sẽ cải thiện hoàn cảnh của con cháu Nôbita sau này.',
                  author='Fujiko F. Fujio', price=18000, inventory=200, category_id=3,
                  image='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSAwIP2EQXwVujdXNrUTon1RvIaCIzMDiYXEg&usqp=CAU')
        p3 = Book(name='100 bí ẩn đáng kinh ngạc về Khoa học',
                  description='Cuốn sách "100 bí ẩn đáng kinh ngạc về khoa học" là một tài liệu hấp dẫn và độc đáo, tập trung vào các khía cạnh kỳ diệu của khoa học. \
                                    Cuốn sách được nghiên cứu kỹ lưỡng và đáng tin cậy, mang đến những thông tin khoa học chính xác và cập nhật. \
                                    Điều này giúp độc giả hiểu rõ và khám phá những khía cạnh thú vị và phức tạp của khoa học. Cuốn sách sử dụng một cách trình bày hài hước, sáng tạo và dễ hiểu để \
                                    truyền tải thông tin khoa học phức tạp một cách đơn giản và gần gũi với độc giả. Nhờ đó, sách trở nên hấp dẫn và thú vị đối với cả trẻ em và người lớn.',
                  author='Nhiều tác giả', price=245000, inventory=200, category_id=2,
                  image='https://dinhtibooks.com.vn/images/products/large/3d_khoa_hoc.webp')
        p4 = Book(name='Khám phá thế giới tâm linh',
                  description='Bằng những trải nghiệm sống động từ chính cuộc đời mình, cùng với đầu óc khoa học cởi mở, \
                                          tiếp thu cả những tinh hoa triết lý phương Đông và phương Tây, tác giả Gary Zukav muốn chia sẻ \
                                          với mọi người những hiểu biết về thế giới nội tâm của con người qua một cách nhìn khác.',
                  author='Gary Zukav', price=78000, inventory=200, category_id=4,
                  image='https://www.sachkhaitri.com/Data/Sites/2/Product/33906/kham-pha-the-gioi-tam-linh.jpg')
        p5 = Book(name='Thất Tịch Không Mưa',
                  description='Thất tịch không mưa kể về câu chuyện tình yêu của Thẩm Hàn Vũ và Thẩm Thiên Tình, một mối tình đã được định trước không có \
                              kết quả tốt, bởi vì họ là anh - em, bởi vì thế sự trên đời, loạn luân là tội ác, là trái ngược với luân thường đạo lý.', \
                  author='Lâu Vũ Tình', price=55000, inventory=200, category_id=3,
                  image='https://img.dtruyen.com/public/images/large/thattichkhongmuaBZ1iPAfFKG.jpg')
        p6 = Book(name='Tâm Lý Học Tội Phạm',
                  description='"Tâm lý học tội phạm" là bộ sách gồm 2 tập đề cập đến quyền lựa chọn, ý chí tự do, cái thiện và cái ác,\
                                phản ứng trước cám dỗ và sự thể hiện lòng dũng cảm hay hèn nhát khi đối mặt với nghịch cảnh của con người.\
                                 Những cuốn sách thiêng liêng của các tôn giáo đều khuyên loài người không nên lừa dối, giận dữ và kiêu ngạo.', \
                  author='Stanton E. Samenow', price=130000, inventory=200, category_id=5,
                  image='https://dnamedical.vn/wp-content/uploads/2023/10/tam-ly-hoc-toi-pham-tap-1-pdf.jpg')
        p7 = Book(name='Conan Tập 1',
                  description='Kudo Shinichi, 17 tuổi, là một thám tử học sinh trung học phổ thông rất nổi tiếng, thường xuyên giúp cảnh sát phá các vụ án khó khăn.\
                               Trong một lần khi đang theo dõi một vụ tống tiền, cậu đã bị thành viên của Tổ chức Áo đen bí ẩn phát hiện.',
                  author='Aoyama Gōshō', price=20000, inventory=200, category_id=3,
                  image='https://img.websosanh.vn/v2/users/root_product/images/tham-tu-lung-danh-conan-tap/UaFkrHlt0Oay.jpg')
        p8 = Book(name='Câu Chuyện Nghệ Thuật',
                  description='Đây là cuốn cẩm nang về các trào lưu, các tác phẩm, chủ đề và kỹ thuật chính yếu trong nghệ thuật. Cuốn sách được viết bởi Susie Hodge,\
                                một nhà sử học nghệ thuật, một sử gia và một họa sĩ. Cô là tác giả ăn khách với nhiều tựa sách về nghệ thuật rất nổi tiếng.',
                  author='Susie Hodge', price=200000, inventory=200, category_id=2,
                  image='https://salt.tikicdn.com/cache/750x750/ts/product/08/28/99/a1866ce83f89de4b846e3630d653aa9a.jpg.webp')
        db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8])
        db.session.commit()
