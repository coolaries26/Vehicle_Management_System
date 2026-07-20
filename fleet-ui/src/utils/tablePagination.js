const tablePagination = {
  defaultPageSize: 10,
  showSizeChanger: true,
  pageSizeOptions: [
    "10",
    "20",
    "50",
    "100",
  ],
  showTotal: (total) =>
    `Total ${total} records`,
};

export default tablePagination;
